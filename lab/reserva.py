"""Trava contra o uso, no LEBRE Lab, da reserva da avaliação final da v0.53.

A lista (lab/reserva_v053.json) é uma cópia de lebre-research, experiments/LEBRE-V0.53-DATA-01/SPLIT_V053.json. Como o
Lab é o banco de desenvolvimento da v0.53, ele nunca pode carregar essas séries.
"""
import json
from pathlib import Path

import pandas as pd

_R = json.loads((Path(__file__).resolve().parent / "reserva_v053.json").read_text(encoding="utf-8"))
USINAS = set(_R["usinas"])
CAMBIO = set(_R["cambio"])
CARGA_DESDE = pd.Timestamp(_R["carga_a_partir_de"])


class SerieReservada(RuntimeError):
    pass


def checar_usina(nome):
    if nome in USINAS:
        raise SerieReservada(f"usina {nome} é reservada para a avaliação final da v0.53")


def checar_fred(serie):
    if serie in CAMBIO:
        raise SerieReservada(f"{serie} é reservada para a avaliação final da v0.53")


def checar_data(fim, o_que):
    """Carga e meteorologia a partir de 2026 ficam fora do Lab (a carga de 2026 é reservada)."""
    if pd.Timestamp(fim) >= CARGA_DESDE:
        raise SerieReservada(f"{o_que} a partir de {CARGA_DESDE.date()} fica fora do Lab (reserva da v0.53)")
