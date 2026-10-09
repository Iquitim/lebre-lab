"""E15 (registrado depois de uma conta exploratória de 09/10/2026, sem modelo nenhum): fração do erro quadrático total da
referência vinda do maior passo e dos 5 maiores, no período de avaliação. Propriedade dos dados, só descrição.
Uso: python -m diagnosticos.e15_maior_passo"""
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from diagnosticos.e13_comum import ARQ, series
from lab.baselines import Naive, SeasonalNaive, Zero


def main():
    L = ["# E15: peso do maior passo no erro da referência", "",
         "Fração de Σ(R − y)² (t >= 20% de T) vinda do maior passo e dos 5 maiores. Todas as séries do desenvolvimento e das "
         "validações 1 a 4.", "", "| Família | Série | maior passo | 5 maiores | n |", "|---|---|---|---|---|"]
    for fam in ARQ:
        for s in series(fam):
            y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape; ini = int(0.2 * T)
            ref = Zero(d) if s.get("zero_baseline") else (SeasonalNaive(d, s["season"]) if s.get("season") else Naive(d))
            e = ((M.rodar_ref(ref, X, y) - y) ** 2)[ini:]; e = np.sort(e[np.isfinite(e)])[::-1]; tot = e.sum()
            if tot > 0:
                L.append(f"| {fam} | {s['nome']} | {100 * e[0] / tot:.2f}% | {100 * e[:5].sum() / tot:.2f}% | {len(e)} |")
    Path(__file__).with_name("E15_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
