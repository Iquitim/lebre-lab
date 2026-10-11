"""T-A05 (validação 7, análoga a A05, troca de regime): mesmo gerador, sementes novas (analises/VALIDACAO7_PLANO.md)."""
from pathlib import Path

from lab.run import load

ORIG = load(Path(__file__).resolve().parents[1] / "A" / "A05_mudanca_regime.py")
SPEC = dict(id="T-A05", frente="T", pergunta="Validação 7 (análoga a A05).", expectativa="-", criterio="ver plano",
            sementes=list(range(2026101230, 2026101250)), aquecimento=0.2, notas="Gerador de A05.")


def gerar(semente):
    return ORIG.gerar(semente)


def avaliar(resumo, series):
    return "inconclusivo"
