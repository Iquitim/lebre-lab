"""T-A07 (validação 7, análoga a A07, relação intermitente): mesmo gerador, sementes novas (analises/VALIDACAO7_PLANO.md)."""
from pathlib import Path

from lab.run import load

ORIG = load(Path(__file__).resolve().parents[1] / "A" / "A07_intermitente.py")
SPEC = dict(id="T-A07", frente="T", pergunta="Validação 7 (análoga a A07).", expectativa="-", criterio="ver plano",
            sementes=list(range(2026101250, 2026101270)), aquecimento=0.2, notas="Gerador de A07.")


def gerar(semente):
    return ORIG.gerar(semente)


def avaliar(resumo, series):
    return "inconclusivo"
