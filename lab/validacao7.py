"""Validação 7 (v0.54, M5b rascunho 1 e M4 rascunho 1). Regras: analises/VALIDACAO7_PLANO.md (commitadas antes de
qualquer download)."""
import functools
import re

import pandas as pd

from lab import validacao5 as V5

POLUENTES, METEO, ALVOS_PEQUIM = V5.POLUENTES, V5.METEO, V5.ALVOS_PEQUIM


@functools.lru_cache(maxsize=1)
def estacao_pequim():
    """A quarta estação em ordem alfabética (regra do plano): nome e DataFrame horário."""
    z, csvs = V5._arquivos_pequim()
    nomes = sorted((re.search(r"PRSA_Data_(.+?)_\d", n.split("/")[-1]).group(1), n) for n in csvs)
    nome, arq = nomes[3]
    df = pd.read_csv(z.open(arq))
    df.index = pd.to_datetime(df[["year", "month", "day", "hour"]])
    return nome, df[POLUENTES + METEO].astype(float).asfreq("h")
