"""Validação 3 da v0.53 (M2). Regras: analises/VALIDACAO3_PLANO.md (commitadas antes de qualquer download)."""
import functools
import json

import numpy as np
import pandas as pd

from lab import fontes as F
from lab.financas import no_calendario

# ------------------------------------------------------------------ finanças, 2010-2025 (X-C01 a X-C04)
CAMBIOS = {"ringgit": "DEXMAUS", "dolar_taiwan": "DEXTAUS", "rupia_sri_lanka": "DEXSLUS", "rand": "DEXSFUS"}
JUROS = {"juro_3a": "DGS3", "juro_7a": "DGS7", "juro_20a": "DGS20"}


@functools.lru_cache(maxsize=1)
def niveis():
    d = {k: no_calendario(F.fred(v)) for k, v in CAMBIOS.items()}
    d |= {k: no_calendario(F.fred(v)) for k, v in JUROS.items()}
    d |= {"juro_2a": no_calendario(F.fred("DGS2")), "juro_10a": no_calendario(F.fred("DGS10"))}
    return pd.DataFrame(d)


def _retorno(p):
    r = 100 * np.log(p.ffill()).diff()
    r[p.isna()] = np.nan
    return r


def _variacao(p):
    d = p.ffill().diff()
    d[p.isna()] = np.nan
    return d


def retornos():
    n = niveis()
    out = {a: _retorno(n[a]) for a in CAMBIOS}
    out |= {f"d_{j}": _variacao(n[j]) for j in list(JUROS) + ["juro_2a", "juro_10a"]}
    return pd.DataFrame(out)


# ------------------------------------------------------------------ NOAA (X-B07)
ESTACOES = ["8461490", "8447930", "8638610", "8735180", "9410660", "9440910"]
ESTACOES_RESERVA = ["8516945", "8729840"]


def estacao_meta(est):
    """Nome e coordenadas pela API de metadados da NOAA (domínio público)."""
    url = f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{est}.json"
    d = json.loads(F._get(url, F.CACHE / "noaa" / f"meta_{est}.json"))["stations"][0]
    return est, d["name"], float(d["lat"]), float(d["lng"])


# ------------------------------------------------------------------ IBGE via SGS (X-C05)
W_C05_CODIGOS = [("ipca_comercializaveis", 4447), ("ipca_nao_comercializaveis", 4448), ("ipca_nao_duraveis", 10841),
                 ("ipca_semiduraveis", 10842)]
W_C05_RESERVA = [("ipca_artigos_residencia", 1637), ("ipca_comunicacao", 1640)]


@functools.lru_cache(maxsize=1)
def w_c05_alvos():
    from lab.validacao import conferir_codigo
    out = []
    for nome, cod in W_C05_CODIGOS + W_C05_RESERVA:
        if len(out) == 4:
            break
        if conferir_codigo(cod)["ok"]:
            out.append((nome, cod))
    if len(out) < 3:                                       # mínimo 3, como no adendo 1 da validação 2
        raise RuntimeError("X-C05: menos de 3 códigos passam na conferência")
    return out
