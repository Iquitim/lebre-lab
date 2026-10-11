"""U-A05 (validação 6, análoga a A05): mesmo gerador, sementes novas (analises/VALIDACAO6_PLANO.md)."""
from pathlib import Path

from lab.run import load

A05 = load(Path(__file__).resolve().parents[1] / "A" / "A05_mudanca_regime.py")
SPEC = dict(id="U-A05", frente="U", pergunta="Validação 6 da M5a (custo, análoga a A05).", expectativa="-",
            criterio="ver plano", sementes=list(range(20261230, 20261250)), aquecimento=0.2,
            notas="Gerador de A05 (troca da entrada relevante em t = 15000; T = 30000).")


def gerar(semente):
    return A05.gerar(semente)


def avaliar(resumo, series):
    return "inconclusivo"
