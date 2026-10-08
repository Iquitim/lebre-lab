"""Diagnóstico E9 de F6 (plano: diagnosticos/F6_E9_PLANO.md). Só descrição."""
import math
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics
from lab.run import ROOT, load


class RLSVariante(OnlineLinear):
    """OnlineLinear com subconjunto de variáveis: usa_x (índices das entradas), q (defasagens de x), p (do alvo)."""

    def __init__(self, n_inputs, usa_x, p, q):
        super().__init__(n_inputs, p=p, q=q)
        self.usa = np.asarray(usa_x)
        self.k = 1 + p + len(self.usa) * (q + 1)
        self.w = np.zeros(self.k); self.P = np.eye(self.k) * 100.0

    def _features(self, x):
        z = super()._features(x)
        base = z[:1 + self.p]
        xs = z[1 + self.p:].reshape(self.q + 1, self.d)[:, self.usa].ravel()
        return np.concatenate([base, xs])


def main():
    mod = load(ROOT / "scenarios" / M.ARQ["B03"])
    L = ["# Diagnóstico E9 de F6 (B03): resultado", "", "| Série | d | v0.52 | L0 | L0Y | Q8 | TOP3 | COMPLETO |",
         "|---|---|---|---|---|---|---|---|"]
    for i in mod.SPEC["sementes"]:
        s = mod.gerar(i); y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape; ini = int(0.2 * T)
        ok = np.isfinite(y[:ini])
        r = [abs(np.corrcoef(np.nan_to_num(X[:ini][ok, j]), y[:ini][ok])[0, 1]) if np.nanstd(X[:ini, j]) > 0 else 0 for j in range(d)]
        top3 = np.argsort(-np.nan_to_num(np.array(r)))[:3]
        todos = np.arange(d)
        mods = {"L0": RLSVariante(d, todos, 0, 0), "L0Y": RLSVariante(d, todos, 2, 0), "Q8": RLSVariante(d, todos, 0, 8),
                "TOP3": RLSVariante(d, top3, 0, 0), "COMPLETO": OnlineLinear(d)}
        mse = {k: forecast_metrics(y, M.rodar_ref(m, X, y), ini)["mse"] for k, m in mods.items()}
        f52 = M.rodar(M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), porta=False), X, y)
        m52 = forecast_metrics(y, f52, ini)["mse"]
        c = mse["COMPLETO"]
        L.append(f"| {s['nome']} | {d} | {m52 / c:.3f} | " + " | ".join(f"{mse[k] / c:.3f}" for k in ("L0", "L0Y", "Q8", "TOP3"))
                 + " | 1.000 |")
        print(L[-1], "(top3 pela correlação no aquecimento:", [s['entradas'][j] for j in top3], ")", flush=True)
    L += ["", "Valores: MSE ÷ MSE do COMPLETO (o comparador linear online do Lab). TOP3 escolhido pela correlação no trecho de"
          " aquecimento (20% iniciais), só para o diagnóstico."]
    Path(__file__).with_name("F6_E9_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
