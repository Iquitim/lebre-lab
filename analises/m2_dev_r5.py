"""Medição da M2, rascunho 5 (plano: analises/M2_DEV_R5_PLANO.md). Copiado de m2_dev_r5.py (inalterado), com uma
configuração (Q: Fixed Share com taxas variáveis sobre a perda recortada) e conferência do rascunho 2 (config H) em C05 e B06.

Uso: python -m analises.m2_dev_r5 A01 ... CURTAS   |   python -m analises.m2_dev_r5 --resumo
"""
import json
import math
import sys

import numpy as np

from analises import m2_dev as M
from analises.m2_dev_r1 import estrutura
from lab.baselines import Naive, SeasonalNaive, Zero
from lab.metrics import forecast_metrics, structure_metrics
from lab.run import ROOT, load

SAIDA = M.AQUI / "m2dev_r5"
SEMENTE = 20261013
CONFIGS = {"Q": "adahedge_compartilhada"}
CONFERIR_R2 = ("C05", "B06")
CURTAS_FONTES = ["B01", "B02", "B03", "B06", "B07", "C01", "C02", "C03", "C04", "C05"]
N_CURTA = 360
TODAS = M.ORDEM + ["CURTAS"]
FP_LIMITE, FP_LIMITE_ANTIGO = 75, 25


def bloco_curta(fam):
    return 24 if fam.startswith("B") else (12 if fam == "C05" else 20)


def rodar(m, X, y):
    T = len(y); f = np.full(T, np.nan); w = np.full(T, np.nan)
    for t in range(T):
        f[t] = m.step(X[t], None if not math.isfinite(y[t]) else float(y[t])).value
        if m.pesos is not None:
            w[t] = m.pesos[1]
    return f, w


def _series(fam):
    """(família de origem, índice, série) para cada série a rodar."""
    if fam != "CURTAS":
        mod = load(ROOT / "scenarios" / M.ARQ[fam])
        for i in mod.SPEC["sementes"]:
            yield fam, i, mod.gerar(i)
        return
    for f in CURTAS_FONTES:
        mod = load(ROOT / "scenarios" / M.ARQ[f])
        for i in mod.SPEC["sementes"]:
            s = dict(mod.gerar(i))
            if f == "C05" and len(s["y"]) != N_CURTA:
                raise SystemExit(f"C05 deveria ter {N_CURTA} passos, tem {len(s['y'])}")
            s["y"] = np.asarray(s["y"], float)[:N_CURTA]; s["X"] = np.asarray(s["X"], float)[:N_CURTA]
            s["truth"] = None
            ini = int(0.2 * N_CURTA)
            if np.isfinite(s["y"][ini:]).sum() < (N_CURTA - ini) / 2:      # adendo 1 do plano (só disponibilidade)
                print("CURTAS: excluída por falta de alvo observado:", f, s["nome"], flush=True)
                continue
            yield f, i, s


def familia(fam):
    info = M.proto_info()
    curtas = fam == "CURTAS"
    if not curtas:
        mod = load(ROOT / "scenarios" / M.ARQ[fam])
        run_id, reg = M.registro_lebre_mse(mod.SPEC["id"])
    else:
        run_id, reg = None, {}
    r2 = json.loads((M.AQUI / "m2dev_r2" / f"{fam}.json").read_text(encoding="utf-8")) if fam in CONFERIR_R2 else None
    series = []
    reps = {c: {"vs_ref": [], "vs_v052": [], "vs_melhor": []} for c in CONFIGS}
    for k, (origem, i, s) in enumerate(_series(fam)):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape
        season, season2, zero = s.get("season"), s.get("season2"), s.get("zero_baseline")
        refnome = "zero" if zero else ("sazonal" if season else "persistencia")
        ref = Zero(d) if zero else (SeasonalNaive(d, season) if season else Naive(d))
        ini = int(0.2 * T)
        L = bloco_curta(origem) if curtas else M.bloco(fam)
        m52 = M.Lebre053(d, season=season, season2=season2, porta=False)
        f52 = M.rodar(m52, X, y)
        fr = M.rodar_ref(ref, X, y)
        mse52, mser = forecast_metrics(y, f52, ini)["mse"], forecast_metrics(y, fr, ini)["mse"]
        fmelhor = f52 if mse52 <= mser else fr
        reg_mse = reg.get(s["nome"])
        linha = dict(serie=s["nome"], origem=origem, T=T, referencia=refnome, bloco=L, mse_v052=mse52, mse_ref=mser,
                     melhor="v0.52" if mse52 <= mser else "referencia",
                     reproducao_dif_rel=None if reg_mse is None else abs(mse52 - reg_mse) / reg_mse,
                     externas_v052=M.externas(m52.events), custo_v052=m52.cost_per_step, configs={})
        if r2 is not None:
            m1 = M.Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, eps_porta=0.002,
                            recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="adahedge")
            mse1 = forecast_metrics(y, M.rodar(m1, X, y), ini)["mse"]
            antigo = next(x for x in r2["series"] if x["serie"] == s["nome"])["configs"]["H"]["mse"]
            linha["conferencia_r2_dif_rel"] = abs(mse1 - antigo) / antigo
        rng = np.random.default_rng([SEMENTE, TODAS.index(fam), k])
        for c, saida in CONFIGS.items():
            m = M.Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, eps_porta=0.002,
                           recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida=saida)
            f, w = rodar(m, X, y)
            wa = w[ini:]
            dw = np.abs(np.diff(w)); dw = dw[np.isfinite(dw)]
            acima = np.flatnonzero(np.nan_to_num(w) > 0.9)
            r = dict(mse=forecast_metrics(y, f, ini)["mse"], peso_L_medio=float(np.nanmean(wa)) if np.isfinite(wa).any() else None,
                     variacao_peso_por_passo=float(dw.mean()) if dw.size else None,
                     primeiro_peso_L_acima_0_9=int(acima[0]) if acima.size else None,
                     trocas_regime=m.agregador.trocas_regime, eventos_auditoria=m.trocas,
                     externas=M.externas(m.events), custo=m.cost_per_step,
                     acrescimo_custo=m.cost_per_step - m52.cost_per_step, cobertura=m.coverage,
                     estrutura_identica=estrutura(m) == estrutura(m52) and m.base.cost_per_step == m52.cost_per_step)
            if s.get("truth") is not None:
                r["recall"] = structure_metrics(m.events, m.structure, s["truth"])["recall"]
            for chave, comp in (("vs_ref", fr), ("vs_v052", f52), ("vs_melhor", fmelhor)):
                p, rep = M.par_bootstrap(y, f, comp, ini, L, rng)
                r["razao_" + chave[3:]] = p
                reps[c][chave].append(rep)
            linha["configs"][c] = r
        series.append(linha)
    resumo = {}
    for c in CONFIGS:
        out = {}
        for k_, chave in (("vs_ref", "razao_ref"), ("vs_v052", "razao_v052"), ("vs_melhor", "razao_melhor")):
            logs = np.array([math.log(s_["configs"][c][chave]) for s_ in series])
            rr = np.vstack(reps[c][k_]).mean(0)
            rr = rr[np.isfinite(rr)]
            out[k_] = dict(geo=float(np.exp(logs.mean())),
                           ic95=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))])
        out["series_com_externa"] = int(sum(s_["configs"][c]["externas"] > 0 for s_ in series))
        out["acrescimo_custo"] = float(np.mean([s_["configs"][c]["acrescimo_custo"] for s_ in series]))
        out["estrutura_identica"] = all(s_["configs"][c]["estrutura_identica"] for s_ in series)
        out["variacao_peso_por_passo"] = float(np.mean([s_["configs"][c]["variacao_peso_por_passo"] or 0.0 for s_ in series]))
        out["peso_L_medio"] = float(np.mean([s_["configs"][c]["peso_L_medio"] for s_ in series
                                             if s_["configs"][c]["peso_L_medio"] is not None]))
        resumo[c] = out
    res = dict(familia=fam, prototipo=info, execucao_lab_conferida=run_id, B=M.B, semente=SEMENTE,
               series_com_externa_v052=int(sum(s_["externas_v052"] > 0 for s_ in series)),
               max_dif_reproducao=max((s_["reproducao_dif_rel"] or 0.0) for s_ in series),
               max_dif_conferencia_r2=max((s_.get("conferencia_r2_dif_rel") or 0.0) for s_ in series) if r2 else None,
               resumo=resumo, series=series)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(fam, "reprodução v0.52:", res["max_dif_reproducao"], "| conferência r2:", res["max_dif_conferencia_r2"],
          "| Q vs_v052", round(resumo["Q"]["vs_v052"]["geo"], 4), resumo["Q"]["vs_v052"]["ic95"],
          "| Q vs_melhor", round(resumo["Q"]["vs_melhor"]["geo"], 4), resumo["Q"]["vs_melhor"]["ic95"], flush=True)


GRUPO = {1: M.NEG, 2: M.POS, 4: M.NULOS, 5: M.ORDEM + ["CURTAS"], 6: M.ORDEM + ["CURTAS"], 7: ["CURTAS"]}


def _passa(n, r, d, limite_fp=FP_LIMITE):
    return {1: r["vs_ref"]["ic95"][1] <= 1.01, 2: r["vs_v052"]["ic95"][1] <= 1.02,
            4: r["series_com_externa"] <= d["series_com_externa_v052"], 5: r["acrescimo_custo"] <= limite_fp,
            6: r["estrutura_identica"], 7: r["vs_melhor"]["ic95"][1] <= 1.05}[n]


def resumo_geral():
    D = {f: json.loads((SAIDA / f"{f}.json").read_text(encoding="utf-8")) for f in TODAS}
    crits = (1, 2, 4, 5, 6, 7)
    L = ["# Medição da M2, rascunho 5: resultado", "",
         f"Plano: `M2_DEV_R5_PLANO.md`. Protótipo: commit `{D['A01']['prototipo']['commit']}`. B = {M.B}, "
         f"semente {SEMENTE}.", "",
         "Reprodução da v0.52 contra o registro do Lab: maior diferença relativa "
         f"{max(d['max_dif_reproducao'] for d in D.values()):.1e}. Conferência do rascunho 2 (C05, B06, config H): maior "
         f"diferença relativa {max(D[f]['max_dif_conferencia_r2'] for f in CONFERIR_R2):.1e}.", "",
         "| Config | Saída | 1 | 2 (C05 incl.) | 4 | 5 (<= 75) | 6 | 7 CURTAS | 5 com o limite antigo (<= 25) | M2 ÷ melhor, 23 famílias (geo) | Falhas |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    esc = {}
    for c, saida in CONFIGS.items():
        falhas = {n: [f for f in GRUPO[n] if not _passa(n, D[f]["resumo"][c], D[f])] for n in crits}
        ok = {n: not falhas[n] for n in crits}
        antigo = all(_passa(5, D[f]["resumo"][c], D[f], FP_LIMITE_ANTIGO) for f in GRUPO[5])
        geo = float(np.exp(np.mean([math.log(D[f]["resumo"][c]["vs_melhor"]["geo"]) for f in TODAS])))
        esc[c] = (ok, geo)
        L.append(f"| {c} | {saida} | " + " | ".join("sim" if ok[n] else "**não**" for n in crits)
                 + f" | {'sim' if antigo else 'não'} | {geo:.4f} | "
                 + ("; ".join(f"{n}: {', '.join(v)}" for n, v in falhas.items() if v) or "-") + " |")
    aptas = sorted([c for c in CONFIGS if all(esc[c][0].values())], key=lambda c: round(esc[c][1], 3))
    L += ["", f"**Escolha: {aptas[0]} ({CONFIGS[aptas[0]]}).**" if aptas else
          "**Nenhuma configuração atende aos critérios; nenhuma é escolhida.**", ""]
    for c in CONFIGS:
        r = D["C05"]["resumo"][c]["vs_v052"]
        L.append(f"C05, {c}: M2 ÷ v0.52 = {r['geo']:.3f} (IC 95% {r['ic95'][0]:.3f}–{r['ic95'][1]:.3f}); primeiro passo "
                 f"com peso de L > 0,9: {[s_['configs'][c]['primeiro_peso_L_acima_0_9'] for s_ in D['C05']['series']]}.")
    L += ["", "| Família | Config | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | M2 ÷ melhor (IC 95%) | peso L | |Δw|/passo | "
          "séries c/ externa (v0.52) | +custo | estrutura idêntica |", "|---|---|---|---|---|---|---|---|---|---|"]
    for f in TODAS:
        for c in CONFIGS:
            r = D[f]["resumo"][c]
            iv = lambda k: f"{r[k]['geo']:.3f} ({r[k]['ic95'][0]:.3f}–{r[k]['ic95'][1]:.3f})"
            L.append(f"| {f} | {c} | {iv('vs_ref')} | {iv('vs_v052')} | {iv('vs_melhor')} | {r['peso_L_medio']:.3f} | "
                     f"{r['variacao_peso_por_passo']:.4f} | {r['series_com_externa']} ({D[f]['series_com_externa_v052']}) | "
                     f"{r['acrescimo_custo']:.1f} | {r['estrutura_identica']} |")
    L += ["", "## CURTAS por origem (média geométrica de M2 ÷ melhor por série)", "", "| Origem | Q | melhor (v0.52 / ref) |",
          "|---|---|---|"]
    S = D["CURTAS"]["series"]
    for o in CURTAS_FONTES:
        ss = [s_ for s_ in S if s_["origem"] == o]
        g = {c: math.exp(np.mean([math.log(s_["configs"][c]["razao_melhor"]) for s_ in ss])) for c in CONFIGS}
        n52 = sum(s_["melhor"] == "v0.52" for s_ in ss)
        L.append(f"| {o} | {g['Q']:.3f} | {n52} / {len(ss) - n52} |")
    (M.AQUI / "M2_DEV_R5_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[:16]))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo_geral()
    else:
        for f in sys.argv[1:]:
            familia(f)
