"""Medição da M2, rascunho 1 (plano: analises/M2_DEV_R1_PLANO.md). Reaproveita as funções de m2_dev.py sem alterá-lo.

Uso: python -m analises.m2_dev_r1 A01 ...   |   python -m analises.m2_dev_r1 --resumo
"""
import json
import math
import sys

import numpy as np

from analises import m2_dev as M
from lab.baselines import Naive, SeasonalNaive, Zero
from lab.metrics import forecast_metrics, structure_metrics
from lab.run import ROOT, load

SAIDA = M.AQUI / "m2dev_r1"
SEMENTE = 20261009
CONFIGS = {"A1": 0.01, "A5": 0.05}
CONFERIR_R0 = ("C05", "B06")
GRUPO = {1: M.NEG, 2: M.POS, 3: M.ORDEM, 4: M.NULOS, 5: M.ORDEM, 6: M.ORDEM}


def estrutura(m):
    return [(e.t, e.outcome, e.change, e.added, e.removed) for e in m.events if e.change != "gate"]


def familia(fam):
    info = M.proto_info()
    mod = load(ROOT / "scenarios" / M.ARQ[fam])
    run_id, reg = M.registro_lebre_mse(mod.SPEC["id"])
    r0 = json.loads((M.SAIDA / f"{fam}.json").read_text(encoding="utf-8")) if fam in CONFERIR_R0 else None
    series = []
    reps = {c: {"vs_ref": [], "vs_v052": []} for c in CONFIGS}
    for i in mod.SPEC["sementes"]:
        s = mod.gerar(i)
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape
        season, season2, zero = s.get("season"), s.get("season2"), s.get("zero_baseline")
        refnome = "zero" if zero else ("sazonal" if season else "persistencia")
        ref = Zero(d) if zero else (SeasonalNaive(d, season) if season else Naive(d))
        ini = int(0.2 * T)
        m52 = M.Lebre053(d, season=season, season2=season2, porta=False)
        f52 = M.rodar(m52, X, y)
        fr = M.rodar_ref(ref, X, y)
        mse52 = forecast_metrics(y, f52, ini)["mse"]
        reg_mse = reg.get(s["nome"])
        linha = dict(serie=s["nome"], T=T, referencia=refnome, mse_v052=mse52,
                     reproducao_dif_rel=None if reg_mse is None else abs(mse52 - reg_mse) / reg_mse,
                     externas_v052=M.externas(m52.events), custo_v052=m52.cost_per_step, configs={})
        if r0 is not None:
            m0 = M.Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, eps_porta=0.002,
                            recriar=True, alpha_porta=None, observar_quarentena_entradas=False)
            mse0 = forecast_metrics(y, M.rodar(m0, X, y), ini)["mse"]
            antigo = next(x for x in r0["series"] if x["serie"] == s["nome"])["configs"]["R2"]["mse"]
            linha["conferencia_r0_dif_rel"] = abs(mse0 - antigo) / antigo
        rng = np.random.default_rng([SEMENTE, M.ORDEM.index(fam), i])
        for c, alpha in CONFIGS.items():
            m = M.Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, eps_porta=0.002,
                           recriar=True, alpha_porta=alpha, observar_quarentena_entradas=True)
            f = M.rodar(m, X, y)
            portas = [e for e in m.events if e.change == "gate"]
            r = dict(mse=forecast_metrics(y, f, ini)["mse"], trocas=m.trocas, trocas_por_2000=m.trocas / T * 2000,
                     primeira_promocao=next((e.t for e in portas if e.added == "lebre"), None),
                     externas=M.externas(m.events), custo=m.cost_per_step,
                     acrescimo_custo=m.cost_per_step - m52.cost_per_step, cobertura=m.coverage,
                     estrutura_identica=estrutura(m) == estrutura(m52) and m.base.cost_per_step == m52.cost_per_step)
            if s.get("truth") is not None:
                r["recall"] = structure_metrics(m.events, m.structure, s["truth"])["recall"]
            p1, rep1 = M.par_bootstrap(y, f, fr, ini, M.bloco(fam), rng)
            p2, rep2 = M.par_bootstrap(y, f, f52, ini, M.bloco(fam), rng)
            r.update(razao_ref=p1, razao_v052=p2)
            reps[c]["vs_ref"].append(rep1)
            reps[c]["vs_v052"].append(rep2)
            linha["configs"][c] = r
        series.append(linha)
    resumo = {}
    for c in CONFIGS:
        out = {}
        for k, chave in (("vs_ref", "razao_ref"), ("vs_v052", "razao_v052")):
            logs = np.array([math.log(s_["configs"][c][chave]) for s_ in series])
            rr = np.vstack(reps[c][k]).mean(0)
            rr = rr[np.isfinite(rr)]
            out[k] = dict(geo=float(np.exp(logs.mean())),
                          ic95=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))])
        out["trocas_por_2000"] = float(np.mean([s_["configs"][c]["trocas_por_2000"] for s_ in series]))
        out["series_com_externa"] = int(sum(s_["configs"][c]["externas"] > 0 for s_ in series))
        out["acrescimo_custo"] = float(np.mean([s_["configs"][c]["acrescimo_custo"] for s_ in series]))
        out["estrutura_identica"] = all(s_["configs"][c]["estrutura_identica"] for s_ in series)
        resumo[c] = out
    res = dict(familia=fam, prototipo=info, execucao_lab_conferida=run_id, B=M.B, semente=SEMENTE, bloco=M.bloco(fam),
               series_com_externa_v052=int(sum(s_["externas_v052"] > 0 for s_ in series)),
               max_dif_reproducao=max((s_["reproducao_dif_rel"] or 0.0) for s_ in series),
               max_dif_conferencia_r0=max((s_.get("conferencia_r0_dif_rel") or 0.0) for s_ in series) if r0 else None,
               resumo=resumo, series=series)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(fam, "reprodução v0.52:", res["max_dif_reproducao"], "| conferência r0:", res["max_dif_conferencia_r0"],
          "| A1 vs_ref", round(resumo["A1"]["vs_ref"]["geo"], 4), "vs_v052", round(resumo["A1"]["vs_v052"]["geo"], 4),
          flush=True)


def _passa(n, r, d):
    return {1: r["vs_ref"]["ic95"][1] <= 1.01, 2: r["vs_v052"]["ic95"][1] <= 1.02, 3: r["trocas_por_2000"] <= 1,
            4: r["series_com_externa"] <= d["series_com_externa_v052"], 5: r["acrescimo_custo"] <= 25,
            6: r["estrutura_identica"]}[n]


def resumo_geral():
    D = {f: json.loads((SAIDA / f"{f}.json").read_text(encoding="utf-8")) for f in M.ORDEM}
    L = ["# Medição da M2, rascunho 1: resultado", "",
         f"Plano: `M2_DEV_R1_PLANO.md`. Protótipo: commit `{D['A01']['prototipo']['commit']}`. B = {M.B}, "
         f"semente {SEMENTE}.", "",
         "Reprodução da v0.52 contra o registro do Lab: maior diferença relativa "
         f"{max(d['max_dif_reproducao'] for d in D.values()):.1e}. Conferência do rascunho 0 (C05, B06): maior "
         f"diferença relativa {max(D[f]['max_dif_conferencia_r0'] for f in CONFERIR_R0):.1e}.", "",
         "| Config | α_porta | 1 | 2 | 3 | 4 | 5 | 6 | M2 ÷ ref negativas (geo) | Famílias que falham |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    esc = {}
    for c, a in CONFIGS.items():
        falhas = {n: [f for f in GRUPO[n] if not _passa(n, D[f]["resumo"][c], D[f])] for n in range(1, 7)}
        ok = {n: not falhas[n] for n in range(1, 7)}
        neg = float(np.exp(np.mean([math.log(D[f]["resumo"][c]["vs_ref"]["geo"]) for f in M.NEG])))
        esc[c] = (ok, neg)
        L.append(f"| {c} | {a} | " + " | ".join("sim" if ok[n] else "**não**" for n in range(1, 7)) + f" | {neg:.4f} | "
                 + (", ".join(f"{n}: {', '.join(v)}" for n, v in falhas.items() if v) or "-") + " |")
    aptas = sorted([c for c in CONFIGS if all(esc[c][0].values())], key=lambda c: (round(esc[c][1], 3), CONFIGS[c]))
    L += ["", f"**Escolha: {aptas[0]}.**" if aptas else "**Nenhuma configuração atende aos 6 critérios; nenhuma é escolhida.**",
          "", "| Família | Config | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | trocas/2000 | séries c/ externa (v0.52) | +custo | estrutura idêntica |",
          "|---|---|---|---|---|---|---|---|"]
    for f in M.ORDEM:
        for c in CONFIGS:
            r = D[f]["resumo"][c]
            L.append(f"| {f} | {c} | {r['vs_ref']['geo']:.3f} ({r['vs_ref']['ic95'][0]:.3f}–{r['vs_ref']['ic95'][1]:.3f}) | "
                     f"{r['vs_v052']['geo']:.3f} ({r['vs_v052']['ic95'][0]:.3f}–{r['vs_v052']['ic95'][1]:.3f}) | "
                     f"{r['trocas_por_2000']:.2f} | {r['series_com_externa']} ({D[f]['series_com_externa_v052']}) | "
                     f"{r['acrescimo_custo']:.1f} | {r['estrutura_identica']} |")
    (M.AQUI / "M2_DEV_R1_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[:12]))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo_geral()
    else:
        for f in sys.argv[1:]:
            familia(f)
