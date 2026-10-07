"""Medição da M2, rascunho 6 (plano: analises/M2_DEV_R6_PLANO.md): banco de desenvolvimento e base de validação.

Derivado de m2_dev_r5.py (inalterado): uma configuração (R6: Fixed Share com taxas variáveis, troca 2/(t+1)^2, sobre a
perda recortada), as 23 famílias do desenvolvimento e as 10 da validação (analises/VALIDACAO_PLANO.md), conferência do
rascunho 2 (config H) em C05 e B06.

Uso: python -m analises.m2_dev_r6 C05 VC05 ...   |   python -m analises.m2_dev_r6 --resumo
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

SAIDA = M.AQUI / "m2dev_r6"
SEMENTE = 20261014
CONFIGS = {"R6": "adahedge_compartilhada_rapida"}
CONFERIR_R2 = ("C05", "B06")
N_CURTA = 360
FP_LIMITE = 75

ARQ_V = {"VB01": "V/VB01_solar.py", "VB02": "V/VB02_carga.py", "VB06": "V/VB06_eolica.py", "VB07": "V/VB07_mare.py",
         "VC01": "V/VC01_retornos.py", "VC02": "V/VC02_volatilidade.py", "VC03": "V/VC03_niveis.py",
         "VC04": "V/VC04_juros.py", "VC05": "V/VC05_inflacao_mensal.py"}
CURTAS_FONTES = {"CURTAS": ["B01", "B02", "B03", "B06", "B07", "C01", "C02", "C03", "C04", "C05"],
                 "VCURTAS": ["VB01", "VB02", "VB06", "VB07", "VC01", "VC02", "VC03", "VC04", "VC05"]}
DEV = M.ORDEM + ["CURTAS"]
VAL = list(ARQ_V) + ["VCURTAS"]
TODAS = DEV + VAL

GRUPO = {"desenvolvimento": {1: M.NEG, 2: M.POS, 4: M.NULOS, 5: DEV, 6: DEV, 7: ["CURTAS"]},
         "validação": {1: ["VC01", "VC03", "VC04"], 2: ["VB01", "VB02", "VB06", "VB07", "VC02", "VC05"],
                       4: ["VC01", "VC04"], 5: VAL, 6: VAL, 7: ["VCURTAS"]}}


def arq(fam):
    return M.ARQ.get(fam) or ARQ_V[fam]


def bloco(fam):
    if fam in M.ARQ:
        return M.bloco(fam)
    return 168 if fam.startswith("VB") else (12 if fam == "VC05" else 20)


def bloco_curta(fam):
    return 24 if fam.lstrip("V").startswith("B") else (12 if fam.endswith("C05") else 20)


def rodar(m, X, y):
    T = len(y); f = np.full(T, np.nan); w = np.full(T, np.nan)
    for t in range(T):
        f[t] = m.step(X[t], None if not math.isfinite(y[t]) else float(y[t])).value
        if m.pesos is not None:
            w[t] = m.pesos[1]
    return f, w


def _series(fam):
    """(família de origem, índice, série) para cada série a rodar."""
    if fam not in CURTAS_FONTES:
        mod = load(ROOT / "scenarios" / arq(fam))
        for i in mod.SPEC["sementes"]:
            yield fam, i, mod.gerar(i)
        return
    for f in CURTAS_FONTES[fam]:
        mod = load(ROOT / "scenarios" / arq(f))
        for i in mod.SPEC["sementes"]:
            s = dict(mod.gerar(i))
            if f == "C05" and len(s["y"]) != N_CURTA:
                raise SystemExit(f"C05 deveria ter {N_CURTA} passos, tem {len(s['y'])}")
            s["y"] = np.asarray(s["y"], float)[:N_CURTA]; s["X"] = np.asarray(s["X"], float)[:N_CURTA]
            s["truth"] = None
            n = len(s["y"]); ini = int(0.2 * n)
            if np.isfinite(s["y"][ini:]).sum() < (n - ini) / 2:          # adendo 1 de M2_DEV_R2_PLANO.md
                print(f"{fam}: excluída por falta de alvo observado:", f, s["nome"], flush=True)
                continue
            yield f, i, s


def familia(fam):
    info = M.proto_info()
    curtas = fam in CURTAS_FONTES
    if fam in M.ARQ:
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
        L = bloco_curta(origem) if curtas else bloco(fam)
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
            r = dict(mse=forecast_metrics(y, f, ini)["mse"],
                     peso_L_medio=float(np.nanmean(wa)) if np.isfinite(wa).any() else None,
                     variacao_peso_por_passo=float(dw.mean()) if dw.size else None,
                     primeiro_peso_L_acima_0_9=int(acima[0]) if acima.size else None,
                     eventos_auditoria=m.trocas, externas=M.externas(m.events), custo=m.cost_per_step,
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
    r = resumo["R6"]
    print(fam, "reprodução v0.52:", res["max_dif_reproducao"], "| conferência r2:", res["max_dif_conferencia_r2"],
          "| vs_ref", round(r["vs_ref"]["geo"], 4), [round(x, 4) for x in r["vs_ref"]["ic95"]],
          "| vs_v052", round(r["vs_v052"]["geo"], 4), [round(x, 4) for x in r["vs_v052"]["ic95"]],
          "| vs_melhor", round(r["vs_melhor"]["geo"], 4), [round(x, 4) for x in r["vs_melhor"]["ic95"]], flush=True)


def _passa(n, r, d):
    return {1: r["vs_ref"]["ic95"][1] <= 1.01, 2: r["vs_v052"]["ic95"][1] <= 1.02,
            4: r["series_com_externa"] <= d["series_com_externa_v052"], 5: r["acrescimo_custo"] <= FP_LIMITE,
            6: r["estrutura_identica"], 7: r["vs_melhor"]["ic95"][1] <= 1.05}[n]


def resumo_geral():
    D = {f: json.loads((SAIDA / f"{f}.json").read_text(encoding="utf-8")) for f in TODAS if (SAIDA / f"{f}.json").exists()}
    faltam = [f for f in TODAS if f not in D]
    c = "R6"
    L = ["# Medição da M2, rascunho 6: resultado (desenvolvimento e validação)", "",
         f"Plano: `M2_DEV_R6_PLANO.md`. Protótipo: commit `{next(iter(D.values()))['prototipo']['commit']}`. "
         f"B = {M.B}, semente {SEMENTE}.", "",
         "Reprodução da v0.52 contra o registro do Lab (desenvolvimento): maior diferença relativa "
         f"{max(d['max_dif_reproducao'] for d in D.values()):.1e}. Conferência do rascunho 2 (C05, B06): "
         f"{[D[f]['max_dif_conferencia_r2'] for f in CONFERIR_R2 if f in D]}.", "",
         f"Famílias não medidas: {', '.join(faltam) if faltam else 'nenhuma'}.", "",
         "| Base | 1 | 2 | 4 | 5 (<= 75) | 6 | 7 | Falhas |", "|---|---|---|---|---|---|---|---|"]
    tudo_ok = not faltam
    for base, G in GRUPO.items():
        falhas = {n: [f for f in fams if f in D and not _passa(n, D[f]["resumo"][c], D[f])] for n, fams in G.items()}
        ok = {n: not v for n, v in falhas.items()}
        tudo_ok = tudo_ok and all(ok.values())
        L.append(f"| {base} | " + " | ".join("sim" if ok[n] else "**não**" for n in (1, 2, 4, 5, 6, 7)) + " | "
                 + ("; ".join(f"{n}: {', '.join(v)}" for n, v in falhas.items() if v) or "-") + " |")
    L += ["", "**Escolha: R6 vai à avaliação final na reserva.**" if tudo_ok else
          "**R6 não é escolhida** (falha em algum critério, ou medição incompleta).", "",
          "| Família | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | M2 ÷ melhor (IC 95%) | peso L | séries c/ externa (v0.52) | "
          "+custo | estrutura idêntica |", "|---|---|---|---|---|---|---|---|"]
    for f in TODAS:
        if f not in D:
            continue
        r = D[f]["resumo"][c]
        iv = lambda k: f"{r[k]['geo']:.3f} ({r[k]['ic95'][0]:.3f}–{r[k]['ic95'][1]:.3f})"
        L.append(f"| {f} | {iv('vs_ref')} | {iv('vs_v052')} | {iv('vs_melhor')} | {r['peso_L_medio']:.3f} | "
                 f"{r['series_com_externa']} ({D[f]['series_com_externa_v052']}) | {r['acrescimo_custo']:.1f} | "
                 f"{r['estrutura_identica']} |")
    (M.AQUI / "M2_DEV_R6_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[:14]))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo_geral()
    else:
        for f in sys.argv[1:]:
            familia(f)
