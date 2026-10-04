"""Ativos e taxas usados na Frente C (fontes e licenças em dados/FONTES.md)."""
import functools

import pandas as pd

from lab import fontes as F
from lab.financas import no_calendario, retorno, variacao


@functools.lru_cache(maxsize=1)
def niveis():
    return pd.DataFrame({
        "dolar_real": no_calendario(F.bcb_sgs(1, 2010, 2025)),          # R$ por US$, PTAX venda (BCB)
        "euro_dolar": no_calendario(F.fred("DEXUSEU")),                 # US$ por euro (Fed H.10)
        "iene_dolar": no_calendario(F.fred("DEXJPUS")),                 # ienes por US$ (Fed H.10)
        "petroleo_wti": no_calendario(F.fred("DCOILWTICO")),            # US$ por barril (EIA)
        "juro_3m": no_calendario(F.fred("DTB3")), "juro_2a": no_calendario(F.fred("DGS2")),
        "juro_10a": no_calendario(F.fred("DGS10")),                      # % ao ano (Fed H.15)
    })


ATIVOS = ["dolar_real", "euro_dolar", "iene_dolar", "petroleo_wti"]
JUROS = ["juro_3m", "juro_2a", "juro_10a"]


def retornos():
    n = niveis()
    return pd.DataFrame({a: retorno(n[a]) for a in ATIVOS} | {f"d_{j}": variacao(n[j]) for j in JUROS})
