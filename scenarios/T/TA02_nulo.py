"""T-A02 (validação 7, análoga a A02, nulo): mesmo gerador, sementes novas (analises/VALIDACAO7_PLANO.md)."""
from pathlib import Path

from lab.run import load

ORIG = load(Path(__file__).resolve().parents[1] / "A" / "A02_nulo.py")
SPEC = dict(id="T-A02", frente="T", pergunta="Validação 7 (análoga a A02).", expectativa="-", criterio="ver plano",
            sementes=list(range(2026101270, 2026101290)), aquecimento=0.2, notas="Gerador de A02.")


def gerar(semente):
    return ORIG.gerar(semente)


def avaliar(resumo, series):
    return "inconclusivo"
