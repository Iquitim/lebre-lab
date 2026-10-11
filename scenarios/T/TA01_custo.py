"""T-A01 (validação 7, análoga a A01): mesmo gerador, sementes novas (analises/VALIDACAO7_PLANO.md)."""
import numpy as np

from lab.synth import base_truth

GRUPOS = {10: range(2026101200, 2026101210), 20: range(2026101210, 2026101220), 50: range(2026101220, 2026101230)}
SPEC = dict(id="T-A01", frente="T", pergunta="Validação 7 (custo, análoga a A01).", expectativa="-",
            criterio="ver plano", sementes=[s for r in GRUPOS.values() for s in r], aquecimento=0.2,
            notas="y = 0,7 x0(t-3) + 0,5 x1(t-10) + ruído 0,7; entradas AR(1) 0,5; T = 20000 (gerador de A01).")


def gerar(semente):
    d = next(k for k, r in GRUPOS.items() if semente in r)
    X, y = base_truth(np.random.default_rng(semente), 20000, d)
    return dict(nome=f"d{d}_s{semente}", grupo=f"d{d}", y=y, X=X, truth=dict(relevant=["x0", "x1"]))


def avaliar(resumo, series):
    return "inconclusivo"
