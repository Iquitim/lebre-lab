"""Montagem das séries financeiras (Frente C).

Calendário: todos os dias úteis de segunda a sexta. Feriados de cada mercado ficam como faltantes (o alvo faltante não é
aprendido; a entrada faltante é preenchida com o último valor, pela LEBRE e pelos comparadores).

Sem olhar o futuro: as entradas entram com 1 dia útil de atraso. O retorno de outro mercado no mesmo dia só é conhecido
junto com o alvo, então usá-lo seria trapaça.
"""
import numpy as np
import pandas as pd

INICIO, FIM = "2010-01-01", "2025-12-31"
DIAS = pd.bdate_range(INICIO, FIM)


def no_calendario(s):
    s = s[~s.index.duplicated()]
    return s.reindex(DIAS)


def retorno(nivel):
    """Retorno logarítmico diário em %, no calendário; NaN onde o próprio dia não tem cotação."""
    p = no_calendario(nivel)
    r = 100 * np.log(p.ffill()).diff()
    r[p.isna()] = np.nan
    return r


def variacao(nivel):
    """Variação diária (ex. de uma taxa de juros, em pontos percentuais), NaN onde o dia não tem cotação."""
    p = no_calendario(nivel)
    d = p.ffill().diff()
    d[p.isna()] = np.nan
    return d


def defasar(df):
    """Entradas com 1 dia útil de atraso."""
    return df.shift(1)
