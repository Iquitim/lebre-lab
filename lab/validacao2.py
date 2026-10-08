"""Validação 2 da v0.53 (M2). Regras: analises/VALIDACAO2_PLANO.md (commitadas antes de qualquer download)."""
import functools
import json

import numpy as np
import pandas as pd

from lab import fontes as F
from lab.financas import no_calendario

# ------------------------------------------------------------------ finanças, 2010-2025 (W-C01 a W-C04)
CAMBIOS = {"rupia": "DEXINUS", "dolar_singapura": "DEXSIUS", "baht": "DEXTHUS", "coroa_dinamarquesa": "DEXDNUS"}
JUROS = {"juro_1a": "DGS1", "juro_5a": "DGS5", "juro_30a": "DGS30"}


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


# ------------------------------------------------------------------ NOAA (W-B07)
ESTACOES = ["8454000", "8658120", "8452660", "8545240", "9418767", "9435380"]
ESTACOES_RESERVA = ["8516945", "8729840"]


def estacao_meta(est):
    """Nome e coordenadas pela API de metadados da NOAA (domínio público)."""
    url = f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{est}.json"
    d = json.loads(F._get(url, F.CACHE / "noaa" / f"meta_{est}.json"))["stations"][0]
    return est, d["name"], float(d["lat"]), float(d["lng"])


# ------------------------------------------------------------------ IBGE via SGS (W-C05)
W_C05_CODIGOS = [("ipca_habitacao", 1636), ("ipca_transportes", 1639), ("ipca_saude", 1641), ("ipca_educacao", 1643)]
W_C05_RESERVA = [("ipca_vestuario", 1638), ("ipca_despesas_pessoais", 1642)]


@functools.lru_cache(maxsize=1)
def w_c05_alvos():
    from lab.validacao import conferir_codigo
    out = []
    for nome, cod in W_C05_CODIGOS + W_C05_RESERVA:
        if len(out) == 4:
            break
        if conferir_codigo(cod)["ok"]:
            out.append((nome, cod))
    if len(out) < 3:                                       # adendo 1 de VALIDACAO2_PLANO.md: mínimo 3
        raise RuntimeError("W-C05: menos de 3 códigos passam na conferência")
    return out
