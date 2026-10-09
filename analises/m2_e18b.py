"""Experimento E18b (plano: analises/E18B_PLANO.md): M2 candidata Q2 (saida="prod_q2") sozinha e com a M1 rascunho 4
(precisao="r4"), régua com os adendos 1 e 2. Derivado de m2_e16b.py (inalterado); além do E16b, conta os passos de
avaliação com previsão não finita (auditoria permanente, E18). Linhagem: m2_e16.py (E16) → m2_e16b.py (E16b) → este.

Uso: python -m analises.m2_e18b CONFIG FAM ...   (CONFIG = q2 | q2_r4)   |   python -m analises.m2_e18b --resumo
"""
import json
import math
import sys

import numpy as np

from analises import m2_dev as M
from analises.m2_dev_r1 import estrutura
from analises import m2_dev_r6 as R6
from analises import m2_val2 as V2
from analises import m2_val3 as X3
from analises import m1_val4 as Y4
from analises.m2_dev_r6 import rodar
from lab.baselines import Naive, SeasonalNaive, Zero
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

AQUI = M.AQUI
SEMENTE, SEMENTE_CLASSE = 20261045, 20261046
N_CURTA = 360
FP_LIMITE = 150
CHOQUE = 0.05
CONFIGS = {"q2": False, "q2_r4": "r4"}
ARQ = dict(M.ARQ) | dict(R6.ARQ_V) | dict(V2.ARQ) | dict(X3.ARQ) | dict(Y4.ARQ)
CURTAS = {"CURTAS": R6.CURTAS_FONTES["CURTAS"], "VCURTAS": R6.CURTAS_FONTES["VCURTAS"], "WCURTAS": list(V2.ARQ),
          "XCURTAS": list(X3.ARQ), "YCURTAS": list(Y4.ARQ)}
TODAS = list(ARQ) + list(CURTAS)
NULOS = ["A02", "C01", "C04", "VC01", "VC04", "WC01", "WC04", "XC01", "XC04", "YC01", "YC04"]
CLASSES = ("v0.52 melhor", "referência melhor", "indecidível", "indecidível (choque)")


def _tipo(fam):
    return fam[1:] if fam[0] in "VWXY" and fam[1] in "BC" else fam


def bloco(fam):
    t = _tipo(fam)
    return 168 if t.startswith("B") else (12 if t == "C05" else 20)


def bloco_curta(fam):
    t = _tipo(fam)
    return 24 if t.startswith("B") else (12 if t == "C05" else 20)


def _series(fam):
    if fam not in CURTAS:
        mod = load(ROOT / "scenarios" / ARQ[fam])
        for i in mod.SPEC["sementes"]:
            try:
                s = mod.gerar(i)
            except IndexError:
                return
            yield fam, s
        return
    for f in CURTAS[fam]:
        mod = load(ROOT / "scenarios" / ARQ[f])
        for i in mod.SPEC["sementes"]:
            try:
                s = dict(mod.gerar(i))
            except IndexError:
                break
            s["y"] = np.asarray(s["y"], float)[:N_CURTA]
            s["X"] = np.asarray(s["X"], float)[:N_CURTA]
            s["truth"] = None
            n = len(s["y"])
            ini = int(0.2 * n)
            if np.isfinite(s["y"][ini:]).sum() < (n - ini) / 2:
                print(fam, "excluída por falta de alvo observado:", f, s["nome"], flush=True)
                continue
            yield f, s


def _ic(rep):
    rep = rep[np.isfinite(rep)]
    return [float(np.exp(np.quantile(rep, 0.025))), float(np.exp(np.quantile(rep, 0.975)))]


def familia(config, fam):
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
        er = ((fr - y) ** 2)[ini:]
        er = er[np.isfinite(er)]
        choque = float(er.max() / er.sum()) if er.size and er.sum() > 0 else 0.0
        pc, repc = M.par_bootstrap(y, f52, fr, ini, L, np.random.default_rng([SEMENTE_CLASSE, TODAS.index(fam), k]))
        icc = _ic(repc)
        classe = "v0.52 melhor" if icc[1] < 1 else ("referência melhor" if icc[0] > 1 else "indecidível")
        if classe in ("referência melhor", "v0.52 melhor") and choque > CHOQUE:   # adendos 1 e 2 de 09/10
            classe = "indecidível (choque)"
        m = M.Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, eps_porta=0.002, recriar=True,
                       alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod_q2", precisao=CONFIGS[config])
        f, w = rodar(m, X, y)
        nan_aval = int((np.isfinite(y) & ~np.isfinite(f))[ini:].sum())
        rng = np.random.default_rng([SEMENTE, TODAS.index(fam), k, list(CONFIGS).index(config)])
        fmelhor = f52 if mse52 <= mser else fr
        r = dict(serie=s["nome"], origem=origem, T=T, d=d, nan_aval=nan_aval, referencia=refnome, bloco=L, classe=classe, choque=choque,
                 v052_sobre_ref=pc, v052_sobre_ref_ic95=icc, mse=forecast_metrics(y, f, ini)["mse"],
                 externas=M.externas(m.events), externas_v052=M.externas(m52.events),
                 acrescimo_custo=m.cost_per_step - m52.cost_per_step, custo_v052=m52.cost_per_step,
                 estrutura_identica=estrutura(m) == estrutura(m52) and m.base.cost_per_step == m52.cost_per_step)
        for chave, comp in (("ref", fr), ("v052", f52), ("melhor", fmelhor)):
            p, rep = M.par_bootstrap(y, f, comp, ini, L, rng)
            r["razao_" + chave] = p
            r["ic95_" + chave] = _ic(rep)
            reps[chave].append(rep)
        series.append(r)
        print(config, fam, s["nome"], classe, "| /ref", round(r["razao_ref"], 4), "/v052", round(r["razao_v052"], 4),
              flush=True)

    def agregado(chave, idx):
        if not idx:
            return None
        logs = np.array([math.log(series[i]["razao_" + chave]) for i in idx])
        rr = np.vstack([reps[chave][i] for i in idx]).mean(0)
        return dict(geo=float(np.exp(logs.mean())), ic95=_ic(rr), n=len(idx))

    idx_ref = [i for i, s_ in enumerate(series) if s_["classe"] == "referência melhor"]
    idx_52 = [i for i, s_ in enumerate(series) if s_["classe"] == "v0.52 melhor"]
    todas = list(range(len(series)))
    resumo = dict(c1=agregado("ref", idx_ref), c2=agregado("v052", idx_52),
                  c7=agregado("melhor", todas) if curtas else None,
                  todas_vs_ref=agregado("ref", todas), todas_vs_v052=agregado("v052", todas),
                  series_com_externa=int(sum(s_["externas"] > 0 for s_ in series)),
                  series_com_externa_v052=int(sum(s_["externas_v052"] > 0 for s_ in series)),
                  acrescimo_custo=float(np.mean([s_["acrescimo_custo"] for s_ in series])),
                  acrescimo_custo_max=float(np.max([s_["acrescimo_custo"] for s_ in series])),
                  estrutura_identica=all(s_["estrutura_identica"] for s_ in series),
                  nan_aval=int(sum(s_["nan_aval"] for s_ in series)),
                  classes={c: sum(s_["classe"] == c for s_ in series) for c in CLASSES})
    res = dict(config=config, familia=fam, prototipo=info, semente=SEMENTE, semente_classe=SEMENTE_CLASSE, B=M.B,
               resumo=resumo, series=series)
    saida = AQUI / f"e18b_{config}"
    saida.mkdir(exist_ok=True)
    (saida / f"{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                       newline="\n")
    print(config, fam, "classes", resumo["classes"], "| c1", resumo["c1"], "| c2", resumo["c2"], "| c7", resumo["c7"],
          flush=True)


def _fmt(a):
    if not a:
        return "-"
    return f"{a['geo']:.3f} ({a['ic95'][0]:.3f}–{a['ic95'][1]:.3f}; n = {a['n']})"


def resumo_geral():
    L = ["# Experimento E18b (Q2 e M1 r4; régua com os adendos 1 e 2): resultado", "",
         "Plano `E18B_PLANO.md`. Régua por decidibilidade com os adendos 1 e 2 de 09/10/2026 (choque > 5% → indecidível nos critérios 1 e 2).",
         ""]
    for config, nome in (("q2", "M2 candidata Q2 sozinha"), ("q2_r4", "M1 rascunho 4 + M2 candidata Q2")):
        pasta = AQUI / f"e18b_{config}"
        D = {f: json.loads((pasta / f"{f}.json").read_text(encoding="utf-8")) for f in TODAS
             if (pasta / f"{f}.json").exists()}
        if not D:
            continue
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
            if config == "q2" and r["acrescimo_custo_max"] > FP_LIMITE:
                falhas[5].append(f)
            if not r["estrutura_identica"]:
                falhas[6].append(f)
            if r["c7"] and r["c7"]["ic95"][1] > 1.05:
                falhas[7].append(f)
            if r["nan_aval"]:
                falhas.setdefault("NaN", []).append(f)
        ok = not faltam and not any(falhas.values())
        commit = next(iter(D.values()))["prototipo"]["commit"]
        L += [f"## {nome}", "", f"Protótipo `{commit}`. Famílias não medidas: {', '.join(faltam) if faltam else 'nenhuma'}.",
              "", "| Critério | Falhas |", "|---|---|"]
        L += [f"| {n} | {', '.join(v) or '-'} |" for n, v in falhas.items()]
        nota = "" if config == "q2" else " (critério 5 só reportado com a M1)"
        L += ["", f"**{'Atende' if ok else 'Não atende'} aos critérios da M2.**{nota}", "",
              "| Família | v0.52 melhor / ref. melhor / indecidível / choque | 1 | 2 | 7 | todas ÷ v0.52 | +custo (máx) | "
              "externas (v0.52) |", "|---|---|---|---|---|---|---|---|"]
        for f in TODAS:
            if f not in D:
                continue
            r = D[f]["resumo"]
            c = r["classes"]
            L.append(f"| {f} | {c[CLASSES[0]]} / {c[CLASSES[1]]} / {c[CLASSES[2]]} / {c[CLASSES[3]]} | {_fmt(r['c1'])} | "
                     f"{_fmt(r['c2'])} | {_fmt(r['c7'])} | {_fmt(r['todas_vs_v052'])} | {r['acrescimo_custo']:.0f} "
                     f"({r['acrescimo_custo_max']:.0f}) | {r['series_com_externa']} ({r['series_com_externa_v052']}) |")
        L.append("")
    (AQUI / "E18B_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[:30]))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo_geral()
    else:
        for fam_ in sys.argv[2:]:
            familia(sys.argv[1], fam_)
