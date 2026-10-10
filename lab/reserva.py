"""Trava contra o uso, no LEBRE Lab, das reservas das avaliações finais da v0.53 e da v0.54.

As listas (lab/reserva_v053.json, lab/reserva_v054.json) são cópias de lebre-research,
experiments/LEBRE-V0.53-DATA-01/SPLIT_V053.json e experiments/LEBRE-V0.54-DATA-01/SPLIT_V054.json. Como o Lab é o banco
de desenvolvimento, ele nunca pode carregar essas séries. A reserva da v0.54 inclui a solar de 2026 inteira (separação no
tempo) e as séries de níveis da EIA e do Tesouro dos EUA (recusadas também pelos códigos equivalentes do FRED).
"""
import json
from pathlib import Path

import pandas as pd

_R = json.loads((Path(__file__).resolve().parent / "reserva_v053.json").read_text(encoding="utf-8"))
_R54 = json.loads((Path(__file__).resolve().parent / "reserva_v054.json").read_text(encoding="utf-8"))
USINAS = set(_R["usinas"])                  # reserva da v0.53: lab/usinas.escolher as exclui (não mudar: a ordem
                                            # da seleção, com empates de capacidade, depende desta exclusão)
USINAS_V054 = set(_R54["usinas_eolicas"])   # reserva da v0.54: recusadas ao carregar (checar_usina)
CAMBIO = set(_R["cambio"])
FRED_RESERVADAS = CAMBIO | set(_R54["fred_equivalentes"])
CARGA_DESDE = pd.Timestamp(_R["carga_a_partir_de"])
SOLAR_DESDE = pd.Timestamp(_R54["solar_a_partir_de"])


class SerieReservada(RuntimeError):
    pass


def checar_usina(nome):
    if nome in USINAS or nome in USINAS_V054:
        raise SerieReservada(f"usina {nome} é reservada para uma avaliação final (v0.53 ou v0.54)")


def checar_fred(serie):
    if serie in FRED_RESERVADAS:
        raise SerieReservada(f"{serie} é reservada para uma avaliação final (v0.53 ou v0.54)")


def checar_ons_fator(anos):
    """O Fator de Capacidade do ONS a partir de 2026 é reservado (solar da v0.54, separação no tempo)."""
    if any(pd.Timestamp(f"{a}-01-01") >= SOLAR_DESDE for a in anos):
        raise SerieReservada(f"Fator de Capacidade do ONS a partir de {SOLAR_DESDE.date()} é reservado (v0.54)")


def checar_data(fim, o_que):
    """Carga e meteorologia a partir de 2026 ficam fora do Lab (a carga de 2026 é reservada)."""
    if pd.Timestamp(fim) >= CARGA_DESDE:
        raise SerieReservada(f"{o_que} a partir de {CARGA_DESDE.date()} fica fora do Lab (reserva da v0.53)")
