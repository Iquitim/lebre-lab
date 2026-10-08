"""Diagnóstico E5 da M2 (oráculo; plano: analises/M2_E5_PLANO.md): "switch_mono_exato" nas 43 famílias do
desenvolvimento e das validações 1 e 2 (já gastas para seleção), com a régua por decidibilidade (M2_CANDIDATA_D.md).
Derivado de m2_e4.py (inalterado).

Uso: python -m analises.m2_e5 C05 VC05 WB01 ...   |   python -m analises.m2_e5 --resumo
"""
import json
import math
import sys

import numpy as np

from analises import m2_dev as M
from analises.m2_dev_r1 import estrutura
from analises import m2_dev_r6 as R6
from analises import m2_val2 as V2
from analises.m2_dev_r6 import rodar
from lab.baselines import Naive, SeasonalNaive, Zero
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

SAIDA = M.AQUI / "m2e5"
SEMENTE, SEMENTE_CLASSE = 20261022, 20261023
SAIDA_D = "switch_mono_exato"
N_CURTA = 360
FP_LIMITE = 75
ARQ = dict(M.ARQ) | dict(R6.ARQ_V) | dict(V2.ARQ)
CURTAS = {"CURTAS": R6.CURTAS_FONTES["CURTAS"], "VCURTAS": R6.CURTAS_FONTES["VCURTAS"], "WCURTAS": list(V2.ARQ)}
TODAS = M.ORDEM + ["CURTAS"] + list(R6.ARQ_V) + ["VCURTAS"] + list(V2.ARQ) + ["WCURTAS"]
NULOS = ["A02", "C01", "C04", "VC01", "VC04", "WC01", "WC04"]


def bloco(fam):
    if fam in M.ARQ:
        return M.bloco(fam)
    return R6.bloco(fam) if fam in R6.ARQ_V else V2.bloco(fam)


def bloco_curta(fam):
    return 24 if fam.lstrip("VW").startswith("B") else (12 if fam.endswith("C05") else 20)


def _series(fam):
    if fam not in CURTAS:
        mod = load(ROOT / "scenarios" / ARQ[fam])
        for i in mod.SPEC["sementes"]:
            yield fam, mod.gerar(i)
        return
    for f in CURTAS[fam]:
        mod = load(ROOT / "scenarios" / ARQ[f])
        for i in mod.SPEC["sementes"]:
            s = dict(mod.gerar(i))
            s["y"] = np.asarray(s["y"], float)[:N_CURTA]; s["X"] = np.asarray(s["X"], float)[:N_CURTA]
            s["truth"] = None
            n = len(s["y"]); ini = int(0.2 * n)
            if np.isfinite(s["y"][ini:]).sum() < (n - ini) / 2:
                print(fam, "excluída por falta de alvo observado:", f, s["nome"], flush=True)
                continue
            yield f, s


def _ic(rep):
    rep = rep[np.isfinite(rep)]
    return [float(np.exp(np.quantile(rep, 0.025))), float(np.exp(np.quantile(rep, 0.975)))]


def familia(fam):
    info = M.proto_info()
    curtas = fam in CURTAS
    series, reps = [], {"ref": [], "v052": [], "melhor": []}
    for k, (origem, s) in enumerate(_series(fam)):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape
        season, season2, zero = s.get("season"), s.get("season2"), s.get("zero_baseline")
        refnome = "zero" if zero else ("sazonal" if season else "persistencia")
        ref = Zero(d) if zero else (SeasonalNaive(d, season) if season else Naive(d))
        ini = int(0.2 * T)
        L = bloco_curta(origem) if curtas else bloco(fam)
        m52 = M.Lebre053(d, season=season, season2=season2, porta=False)
        f52 = M.rodar(m52, X, y)
        fr = M.rodar_ref(ref, X, y)
        mse52, mser = forecast_metrics(y, f52, ini)["mse"], forecast_metrics(y, fr, ini)["mse"]
        # classificação (só v0.52 e referência, semente própria)
        pc, repc = M.par_bootstrap(y, f52, fr, ini, L, np.random.default_rng([SEMENTE_CLASSE, TODAS.index(fam), k]))
        icc = _ic(repc)
        classe = "v0.52 melhor" if icc[1] < 1 else ("referência melhor" if icc[0] > 1 else "indecidível")
        m = M.Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, eps_porta=0.002, recriar=True,
                       alpha_porta=0.01, observar_quarentena_entradas=True, saida=SAIDA_D)
        f, w = rodar(m, X, y)
        rng = np.random.default_rng([SEMENTE, TODAS.index(fam), k])
        fmelhor = f52 if mse52 <= mser else fr
        r = dict(serie=s["nome"], origem=origem, T=T, referencia=refnome, bloco=L, classe=classe,
                 v052_sobre_ref=pc, v052_sobre_ref_ic95=icc, mse=forecast_metrics(y, f, ini)["mse"],
                 peso_L_medio=float(np.nanmean(w[ini:])) if np.isfinite(w[ini:]).any() else None,
                 externas=M.externas(m.events), externas_v052=M.externas(m52.events),
                 acrescimo_custo=m.cost_per_step - m52.cost_per_step, cobertura=m.coverage,
                 estrutura_identica=estrutura(m) == estrutura(m52) and m.base.cost_per_step == m52.cost_per_step)
        for chave, comp in (("ref", fr), ("v052", f52), ("melhor", fmelhor)):
            p, rep = M.par_bootstrap(y, f, comp, ini, L, rng)
            r["razao_" + chave] = p; r["ic95_" + chave] = _ic(rep)
            reps[chave].append(rep)
        series.append(r)
        print(fam, s["nome"], classe, "v0.52/ref", round(pc, 3), [round(x, 3) for x in icc], "| D/ref", round(r["razao_ref"], 4),
              "D/v052", round(r["razao_v052"], 4), flush=True)

    def agregado(chave, idx):
        if not idx:
            return None
        logs = np.array([math.log(series[i]["razao_" + chave]) for i in idx])
        rr = np.vstack([reps[chave][i] for i in idx]).mean(0)
        return dict(geo=float(np.exp(logs.mean())), ic95=_ic(rr), n=len(idx))

    idx_ref = [i for i, s_ in enumerate(series) if s_["classe"] == "referência melhor"]
    idx_52 = [i for i, s_ in enumerate(series) if s_["classe"] == "v0.52 melhor"]
    resumo = dict(c1=agregado("ref", idx_ref), c2=agregado("v052", idx_52),
                  c7=agregado("melhor", list(range(len(series)))) if curtas else None,
                  todas_vs_ref=agregado("ref", list(range(len(series)))),
                  todas_vs_v052=agregado("v052", list(range(len(series)))),
                  series_com_externa=int(sum(s_["externas"] > 0 for s_ in series)),
                  series_com_externa_v052=int(sum(s_["externas_v052"] > 0 for s_ in series)),
                  acrescimo_custo=float(np.mean([s_["acrescimo_custo"] for s_ in series])),
                  estrutura_identica=all(s_["estrutura_identica"] for s_ in series),
                  classes={c: sum(s_["classe"] == c for s_ in series)
                           for c in ("v0.52 melhor", "referência melhor", "indecidível")})
    res = dict(familia=fam, prototipo=info, semente=SEMENTE, semente_classe=SEMENTE_CLASSE, B=M.B, resumo=resumo,
               series=series)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(fam, "classes", resumo["classes"], "| c1", resumo["c1"], "| c2", resumo["c2"], "| c7", resumo["c7"], flush=True)


def resumo_geral():
    D = {f: json.loads((SAIDA / f"{f}.json").read_text(encoding="utf-8")) for f in TODAS if (SAIDA / f"{f}.json").exists()}
    faltam = [f for f in TODAS if f not in D]
    falhas = {1: [], 2: [], 4: [], 5: [], 6: [], 7: []}
    for f, d in D.items():
        r = d["resumo"]
        if r["c1"] and r["c1"]["ic95"][1] > 1.01:
            falhas[1].append(f)
        if r["c2"] and r["c2"]["ic95"][1] > 1.02:
            falhas[2].append(f)
        if f in NULOS and r["series_com_externa"] > r["series_com_externa_v052"]:
            falhas[4].append(f)
        if r["acrescimo_custo"] > FP_LIMITE:
            falhas[5].append(f)
        if not r["estrutura_identica"]:
            falhas[6].append(f)
        if r["c7"] and r["c7"]["ic95"][1] > 1.05:
            falhas[7].append(f)
    ok = not faltam and not any(falhas.values())
    fmt = lambda a: "-" if not a else f"{a['geo']:.3f} ({a['ic95'][0]:.3f}–{a['ic95'][1]:.3f}; n = {a['n']})"
    L = ["# Diagnóstico E5 da M2 (oráculo da candidata M com escala atual): resultado", "",
         f"Plano: `M2_E5_PLANO.md`. Protótipo: commit `{next(iter(D.values()))['prototipo']['commit']}`. B = {M.B}; "
         f"sementes {SEMENTE} (medição) e {SEMENTE_CLASSE} (classificação).", "",
         f"Famílias não medidas: {', '.join(faltam) if faltam else 'nenhuma'}.", "",
         "| Critério | Falhas |", "|---|---|"] + [f"| {n} | {', '.join(v) or '-'} |" for n, v in falhas.items()] + [
         "", "**O oráculo atende a todos os critérios nas 43 famílias de desenvolvimento.**" if ok else
         "**O oráculo não atende a todos os critérios.**", "",
         "| Família | séries (v0.52 melhor / ref. melhor / indecidível) | 1: M2 ÷ ref nas \"ref. melhor\" | "
         "2: M2 ÷ v0.52 nas \"v0.52 melhor\" | 7: M2 ÷ melhor | todas: M2 ÷ v0.52 | +custo | externas (v0.52) | estrutura |",
         "|---|---|---|---|---|---|---|---|---|"]
    for f in TODAS:
        if f not in D:
            continue
        r = D[f]["resumo"]; c = r["classes"]
        L.append(f"| {f} | {c['v0.52 melhor']} / {c['referência melhor']} / {c['indecidível']} | {fmt(r['c1'])} | "
                 f"{fmt(r['c2'])} | {fmt(r['c7'])} | {fmt(r['todas_vs_v052'])} | {r['acrescimo_custo']:.1f} | "
                 f"{r['series_com_externa']} ({r['series_com_externa_v052']}) | {r['estrutura_identica']} |")
    L += ["", "## Séries indecidíveis (reportadas, sem aprovar nem reprovar)", "",
          "| Família | Série | v0.52 ÷ ref (IC 95%) | M2 ÷ v0.52 | M2 ÷ ref |", "|---|---|---|---|---|"]
    for f in TODAS:
        for s_ in D.get(f, {}).get("series", []):
            if s_["classe"] == "indecidível":
                L.append(f"| {f} | {s_['serie']} | {s_['v052_sobre_ref']:.3f} ({s_['v052_sobre_ref_ic95'][0]:.3f}–"
                         f"{s_['v052_sobre_ref_ic95'][1]:.3f}) | {s_['razao_v052']:.3f} | {s_['razao_ref']:.3f} |")
    (M.AQUI / "M2_E5_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[:20]))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo_geral()
    else:
        for f in sys.argv[1:]:
            familia(f)
