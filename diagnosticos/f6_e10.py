"""Diagnóstico E10 de F6 (plano: diagnosticos/F6_E10_PLANO.md). Só descrição."""
import math
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

BANDAS = [(0, 0), (1, 1), (2, 3), (4, 7), (8, 15)]


class RLSBandas:
    """RLS sobre [1, y_{t-1}, y_{t-2}, bandas das entradas escolhidas]; atualiza a cada `cada` passos."""

    def __init__(self, usa, bandas, cada):
        self.usa = np.asarray(usa); self.bandas = bandas; self.cada = cada
        self.k = 3 + len(self.usa) * len(bandas)
        self.w = np.zeros(self.k); self.P = np.eye(self.k) * 100.0
        self.xh = []; self.yh = []; self.n = 0; self.z = None; self.ult = None

    def _x(self, x):
        x = np.asarray(x, float).copy()
        if self.ult is None:
            self.ult = np.zeros_like(x)
        ok = np.isfinite(x); self.ult[ok] = x[ok]; x[~ok] = self.ult[~ok]
        self.xh.append(x[self.usa])
        if len(self.xh) > 16:
            self.xh.pop(0)
        H = np.array(self.xh[::-1])                            # H[0] = instante t
        feats = []
        for a, b in self.bandas:
            sl = H[a:b + 1] if len(H) > a else np.zeros((1, len(self.usa)))
            feats.append(sl.mean(0) if len(sl) else np.zeros(len(self.usa)))
        ys = [v for v in reversed(self.yh) if math.isfinite(v)][:2]
        ys += [0.0] * (2 - len(ys))
        return np.concatenate([[1.0], ys, np.ravel(np.array(feats).T)])

    def predict(self, x):
        self.z = self._x(x)
        return float(self.w @ self.z)

    def observe(self, y):
        v = math.nan if y is None or not math.isfinite(y) else float(y)
        self.yh.append(v)
        if len(self.yh) > 4:
            self.yh.pop(0)
        if math.isnan(v):
            return
        self.n += 1
        if self.n % self.cada:
            return
        z = self.z; Pz = self.P @ z; g = Pz / (0.999 + z @ Pz)
        self.w = self.w + g * (v - self.w @ z)
        P = (self.P - np.outer(g, Pz)) / 0.999; self.P = (P + P.T) / 2
        if not np.isfinite(self.P).all() or np.diag(self.P).min() <= 0:
            self.P = np.eye(self.k) * 100.0


def fp(k, n_ent, cada):
    return (6 * k * k + 4 * k) / cada + 2 * k + 2 * n_ent * 5


def main():
    mod = load(ROOT / "scenarios" / M.ARQ["B03"])
    res = {}
    for i in mod.SPEC["sementes"]:
        s = mod.gerar(i); y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape; ini = int(0.2 * T)
        ok = np.isfinite(y[:ini])
        r = np.array([abs(np.corrcoef(np.nan_to_num(X[:ini][ok, j]), y[:ini][ok])[0, 1]) for j in range(d)])
        top3 = np.argsort(-np.nan_to_num(r))[:3]
        comp = forecast_metrics(y, M.rodar_ref(OnlineLinear(d), X, y), ini)["mse"]
        f52 = M.rodar(M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), porta=False), X, y)
        v52 = forecast_metrics(y, f52, ini)["mse"]
        linha = {"v0.52": (v52 / comp, None)}
        for nome, usa, bandas in (("AR2+0", np.arange(d), [(0, 0)]), ("AR2+B3", top3, BANDAS), ("AR2+B8", np.arange(d), BANDAS)):
            for cada in (1, 8):
                m = RLSBandas(usa, bandas, cada)
                mse = forecast_metrics(y, M.rodar_ref(m, X, y), ini)["mse"]
                linha[f"{nome}/{cada}"] = (mse / comp, fp(m.k, len(usa), cada))
        for cada in (1, 8):
            k = 1 + 2 + d * 9
            if cada == 1:
                linha["COMPLETO/1"] = (1.0, fp(k, 0, 1))
            else:
                class C8(OnlineLinear):
                    n = 0
                    def observe(self, yy):
                        v = math.nan if yy is None or not math.isfinite(yy) else yy
                        if not math.isnan(v):
                            self.n += 1
                        if math.isnan(v) or self.n % 8:
                            self.hist.append(v); return
                        super().observe(yy)
                mse = forecast_metrics(y, M.rodar_ref(C8(d), X, y), ini)["mse"]
                linha["COMPLETO/8"] = (mse / comp, fp(k, 0, 8))
        res[s["nome"]] = linha
        print(s["nome"], {k_: round(v[0], 3) for k_, v in linha.items()}, flush=True)
    cols = list(next(iter(res.values())).keys())
    L = ["# Diagnóstico E10 de F6: fronteira precisão × custo (B03)", "",
         "MSE ÷ MSE do comparador linear completo atualizado a cada passo. Custo em FP por passo (regra da v0.52) do especialista sozinho.", "",
         "| Série | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
    for nome, linha in res.items():
        L.append(f"| {nome} | " + " | ".join(f"{linha[c][0]:.3f}" for c in cols) + " |")
    geo = {c: math.exp(np.mean([math.log(res[n][c][0]) for n in res])) for c in cols}
    L.append("| **geo** | " + " | ".join(f"**{geo[c]:.3f}**" for c in cols) + " |")
    L.append("| FP/passo | " + " | ".join("-" if next(iter(res.values()))[c][1] is None else f"{next(iter(res.values()))[c][1]:.0f}" for c in cols) + " |")
    Path(__file__).with_name("F6_E10_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[-3:]))


if __name__ == "__main__":
    main()
