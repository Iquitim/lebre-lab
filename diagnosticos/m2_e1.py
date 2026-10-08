"""Diagnóstico E1 da M2 (plano: diagnosticos/M2_E1_PLANO.md). Só descrição."""
import math
import os
import sys
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from lab.baselines import Naive, SeasonalNaive, Zero
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

CASOS = [("C/C04_juros.py", "d_juro_2a"), ("B/B01_solar.py", "Conj. Arinos 2 500 kV"),
         ("V/VC05_inflacao_mensal.py", "ipca_servicos"), ("C/C05_macro_mensal_curta.py", "ipca")]
SAIDAS = {"r4": "adahedge_recortada", "r6": "adahedge_compartilhada_rapida"}


def achar(arq, nome):
    mod = load(ROOT / "scenarios" / arq)
    for i in mod.SPEC["sementes"]:
        s = mod.gerar(i)
        if s["nome"] == nome:
            return s
    raise SystemExit(nome)


def main():
    print("protótipo:", M.proto_info())
    L = ["# Diagnóstico E1 da M2: resultado", ""]
    for arq, nome in CASOS:
        s = achar(arq, nome)
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape
        season, season2, zero = s.get("season"), s.get("season2"), s.get("zero_baseline")
        refnome = "zero" if zero else ("sazonal" if season else "persistencia")
        ref = Zero(d) if zero else (SeasonalNaive(d, season) if season else Naive(d))
        ini = int(0.2 * T)
        f52 = M.rodar(M.Lebre053(d, season=season, season2=season2, porta=False), X, y)
        fr = M.rodar_ref(ref, X, y)
        mse52, mser = forecast_metrics(y, f52, ini)["mse"], forecast_metrics(y, fr, ini)["mse"]
        L += [f"## {nome} (T = {T}, referência {refnome}; v0.52 ÷ ref = {mse52 / mser:.3f})", "",
              "| Config | M2 ÷ v0.52 | M2 ÷ ref | peso L (q10/q50/q90 na avaliação) | fração aval. com peso L > 0,5 | η (q10/q50/q90) | Σ(ℓR − ℓL) em 25/50/75/100% |",
              "|---|---|---|---|---|---|---|"]
        for c, saida in SAIDAS.items():
            m = M.Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, alpha_porta=0.01,
                           observar_quarentena_entradas=True, saida=saida)
            f = np.full(T, np.nan); w = np.full(T, np.nan); eta = []; dif = []; ac = 0.0
            Lant = None
            for t in range(T):
                f[t] = m.step(X[t], None if not math.isfinite(y[t]) else float(y[t])).value
                if m.pesos is not None:
                    w[t] = m.pesos[1]
                ag = m.agregador
                if ag.__class__.__name__ == "Agregador":
                    cum = ag.L.copy()
                    if Lant is not None and not np.array_equal(cum, Lant):
                        eta.append(ag.eta())
                    Lant = cum
                    dif.append(cum[0] - cum[1])
                else:
                    if len(ag.etas) > len(eta):
                        eta.append(ag.etas[-1])
                    dif.append(np.nan)
            mse = forecast_metrics(y, f, ini)["mse"]
            wa = w[ini:]; wa = wa[np.isfinite(wa)]
            et = np.array([e for e in eta if math.isfinite(e)])
            q = lambda a: "/".join(f"{v:.3g}" for v in np.quantile(a, [0.1, 0.5, 0.9])) if len(a) else "-"
            dd = np.array(dif)
            pos = [int(p * (T - 1)) for p in (0.25, 0.5, 0.75, 1.0)]
            ds = "/".join(f"{dd[p]:.1f}" for p in pos) if np.isfinite(dd).any() else "n/d"
            L.append(f"| {c} | {mse / mse52:.4f} | {mse / mser:.4f} | {q(wa)} | {float(np.mean(wa > 0.5)):.2f} | {q(et)} | {ds} |")
            print(nome, c, round(mse / mse52, 4), round(mse / mser, 4), flush=True)
        L.append("")
    Path(__file__).with_name("M2_E1_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
