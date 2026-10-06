"""Diagnóstico F9 (pergunta e regra em F9_PERGUNTA.md). Uso: python -m diagnosticos.F9_niveis"""
import json
import math
from pathlib import Path

import numpy as np

import lebre
from lab.run import ROOT, load

C03 = load(ROOT / "scenarios" / "C" / "C03_niveis_de_preco.py")
W = 250


def rodar(y, X):
    T = len(y); m = lebre.Lebre(X.shape[1]); s = lebre.Lebre(1)
    f, g = np.full(T, np.nan), np.full(T, np.nan)
    for t in range(T):
        yt = None if not math.isfinite(y[t]) else float(y[t])
        f[t] = m.step(X[t], yt).value; g[t] = s.step([0.0], yt).value
    return f, g, m


def mse(y, f, a, b):
    e = (y[a:b] - f[a:b]) ** 2
    e = e[np.isfinite(e)]
    return float(e.mean()) if len(e) else math.nan


def main():
    linhas = []
    for i in C03.SPEC["sementes"]:
        s = C03.gerar(i); y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        f, g, m = rodar(y, X)
        for e in m.events:
            if e.outcome != "accepted" or not e.added or not e.added.startswith("x"):
                continue
            t = e.t; nome = s["entradas"][int(e.added.split("[")[0][1:])]
            antes = mse(y, f, max(0, t - W), t) / mse(y, g, max(0, t - W), t)
            depois = mse(y, f, t + 1, t + 1 + W) / mse(y, g, t + 1, t + 1 + W)
            ate_fim = mse(y, f, t + 1, len(y)) / mse(y, g, t + 1, len(y))
            cls = "nunca existiu" if antes >= 1 else ("existiu e sumiu" if depois >= 1 else "existiu e ficou")
            linhas.append(dict(serie=s["nome"], entrada=nome, passo=t, razao_antes=round(antes, 3),
                               razao_depois=round(depois, 3), razao_ate_o_fim=round(ate_fim, 3), classe=cls))
    out = Path(__file__).with_name("F9_RESULTADO.json")
    out.write_text(json.dumps(linhas, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    for r in linhas:
        print(r)


if __name__ == "__main__":
    main()
