"""Errata 01 da v0.54, segunda medição (plano: analises/ERRATA01_V054_E2_PLANO.md), em 60 séries sintéticas novas.
Usa preparar, rodar e relatorio de analises/errata01_v054.py sem alteração. Uso (da raiz do Lab, com as mesmas variáveis
de ambiente da primeira medição):  python -m analises.errata01_v054_e2 GRUPO ...   |   python -m analises.errata01_v054_e2 resumo
"""
import json
import sys

import numpy as np

import lebre
from analises import errata01_v054 as P
from analises import m5a_e1 as E
from lab.run import ROOT, load
from lab.synth import ar1, base_truth

OUT = E.AQUI / "errata01_v054_e2"
GRUPOS = {"custo_d10": range(2026101410, 2026101420), "custo_d20": range(2026101420, 2026101430),
          "custo_d50": range(2026101430, 2026101440), "troca": range(2026101440, 2026101450),
          "intermitente": range(2026101450, 2026101460), "nulo_d20": range(2026101460, 2026101470)}


def gerar(grupo, sd):
    if grupo.startswith("custo"):
        return base_truth(np.random.default_rng(sd), 20000, int(grupo[7:]))
    if grupo == "troca":
        s = load(ROOT / "scenarios" / "A" / "A05_mudanca_regime.py").gerar(sd); return s["X"], s["y"]
    if grupo == "intermitente":
        s = load(ROOT / "scenarios" / "A" / "A07_intermitente.py").gerar(sd); return s["X"], s["y"]
    rng = np.random.default_rng(sd); T = 20000                       # como A02, com 20 entradas
    X = ar1(rng, T, 20); e = rng.standard_normal(T); y = np.empty(T); y[0] = e[0]
    for t in range(1, T):
        y[t] = 0.6 * y[t - 1] + e[t]
    return X, y


def pendente(m):
    c = m.core._core
    if getattr(c, "_eq_xc", None) is None:
        return 0.0
    return float(sum(3 * (c.d - i) for i in range(c._eq_next, c.d)))


def grupo(g):
    CoreP = P.preparar(); series = []
    for sd in GRUPOS[g]:
        X, y = gerar(g, sd); d = X.shape[1]
        e01, prom, v53 = E.Lebre054(d, **P.KW054), E.Lebre054(d, **P.KW054), lebre.Lebre(d)
        prom.core._core = CoreP(prom.n_inputs)
        fe, ce, _ = P.rodar(e01, X, y); fp, cp, _ = P.rodar(prom, X, y); fv, cv, _ = P.rodar(v53, X, y)
        pend = pendente(e01)                                          # antes da consulta ao relatório
        tot_e, tot_p = float(ce.sum()), float(cp.sum())
        series.append(dict(semente=sd, T=len(y), d=d, identica=bool(np.array_equal(fe, fp, equal_nan=True)),
                           estrutura_igual=e01.structure == prom.structure, relatorio_igual=P.relatorio(e01) == P.relatorio(prom),
                           custo_total_e01=tot_e, pendente=pend, custo_total_prom=tot_p, dif=tot_e + pend - tot_p,
                           pico_e01=float(ce.max()), pico_prom=float(cp.max()), pico_v053=float(cv.max())))
        print(g, sd, {k: v for k, v in series[-1].items() if k != "semente"}, flush=True)
    OUT.mkdir(exist_ok=True)
    (OUT / f"{g}.json").write_text(json.dumps(dict(grupo=g, series=series), indent=1) + "\n", encoding="utf-8", newline="\n")


def resumo():
    R = {g: json.loads((OUT / f"{g}.json").read_text(encoding="utf-8"))["series"] for g in GRUPOS}
    S = [x for v in R.values() for x in v]
    c1 = all(x["identica"] and x["estrutura_igual"] and x["relatorio_igual"] for x in S)
    c2 = all(abs(x["dif"]) <= 1e-6 for x in S)
    linhas, falha3 = [], []
    for g, ss in R.items():
        pe, pp, pv = max(x["pico_e01"] for x in ss), max(x["pico_prom"] for x in ss), max(x["pico_v053"] for x in ss)
        linhas.append(f"| {g} | {len(ss)} | {pv:.0f} | {pp:.0f} | {pe:.0f} | {pe / pv:.3f} | {max(abs(x['dif']) for x in ss):.2e} |")
        if pe > 1.10 * pv:
            falha3.append(g)
    c3 = not falha3
    L = ["# Errata 01 da v0.54, segunda medição (dados novos): resultado", "",
         f"Plano `ERRATA01_V054_E2_PLANO.md`. {len(S)} séries sintéticas novas.", "",
         "| Grupo | séries | pico v0.53 | pico v0.54 promovida | pico v0.54 com errata | errata ÷ v0.53 | maior diferença de custo (critério 2) |",
         "|---|---|---|---|---|---|---|"] + linhas
    L += ["", f"1. **Identidade com a v0.54 promovida:** {'atende' if c1 else 'não atende'}",
          f"2. **Custo total igual, contando as linhas pendentes no fim:** {'atende' if c2 else 'não atende'}",
          f"3. **Pico ≤ 1,10 × o da v0.53 em cada grupo:** {'atende' if c3 else 'não atende: ' + ', '.join(falha3)}", "",
          f"**Decisão pela regra do plano:** a errata 01 é **{'aceita' if c1 and c2 and c3 else 'não aceita'}**."]
    (E.AQUI / "ERRATA01_V054_E2_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("feito")


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for g in sys.argv[1:]:
            grupo(g)
