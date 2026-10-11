"""Validação 6 (v0.54, M5a rascunho 2). Regras: analises/VALIDACAO6_PLANO.md (commitadas antes de qualquer download)."""
import functools
import re

import pandas as pd

from lab import validacao5 as V5

POLUENTES, METEO, ALVOS_PEQUIM = V5.POLUENTES, V5.METEO, V5.ALVOS_PEQUIM
ESTACOES = ["9419750", "8770570", "8723214", "9410170", "9455920", "1612340"]
ESTACOES_RESERVA = ["8726724", "9751639"]


@functools.lru_cache(maxsize=1)
def estacao_pequim():
    """A terceira estação em ordem alfabética (regra do plano): nome e DataFrame horário."""
    z, csvs = V5._arquivos_pequim()
    nomes = sorted((re.search(r"PRSA_Data_(.+?)_\d", n.split("/")[-1]).group(1), n) for n in csvs)
    nome, arq = nomes[2]
    df = pd.read_csv(z.open(arq))
    df.index = pd.to_datetime(df[["year", "month", "day", "hour"]])
    return nome, df[POLUENTES + METEO].astype(float).asfreq("h")


def estacao_meta(est):
    from lab.validacao2 import estacao_meta as m
    return m(est)
