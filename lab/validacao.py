"""Base de validação da v0.53 (M2). Regras: analises/VALIDACAO_PLANO.md (commitadas antes de qualquer download).

Funções próprias para os períodos e listas da validação; o código do banco de desenvolvimento não é alterado.
"""
import functools

import numpy as np
import pandas as pd

from lab import fontes as F

# ------------------------------------------------------------------ finanças, 2000-2009 (VC01-VC04)
DIAS = pd.bdate_range("2000-01-01", "2009-12-31")
ATIVOS = ["dolar_real", "euro_dolar", "iene_dolar", "petroleo_wti"]
JUROS = ["juro_3m", "juro_2a", "juro_10a"]


def _cal(s):
    return s[~s.index.duplicated()].reindex(DIAS)


@functools.lru_cache(maxsize=1)
def niveis():
    return pd.DataFrame({
        "dolar_real": _cal(F.bcb_sgs(1, 2000, 2009)), "euro_dolar": _cal(F.fred("DEXUSEU")),
        "iene_dolar": _cal(F.fred("DEXJPUS")), "petroleo_wti": _cal(F.fred("DCOILWTICO")),
        "juro_3m": _cal(F.fred("DTB3")), "juro_2a": _cal(F.fred("DGS2")), "juro_10a": _cal(F.fred("DGS10")),
    })


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
    return pd.DataFrame({a: _retorno(n[a]) for a in ATIVOS} | {f"d_{j}": _variacao(n[j]) for j in JUROS})


# ------------------------------------------------------------------ NOAA (VB07)
ESTACOES = [("8574680", "Baltimore", 39.2669, -76.5794), ("8726520", "St. Petersburg", 27.7606, -82.6269),
            ("8761724", "Grand Isle", 29.2633, -89.9567), ("9414290", "San Francisco", 37.8063, -122.4659),
            ("9447130", "Seattle", 47.6026, -122.3393), ("9410230", "La Jolla", 32.8669, -117.2571)]
ESTACOES_RESERVA = [("8454000", "Providence", 41.8072, -71.4006), ("8658120", "Wilmington", 34.2275, -77.9536)]

# ------------------------------------------------------------------ IBGE via SGS (VC05)
VC05_CODIGOS = [("ipca15", 7478), ("ipca_alimentos_bebidas", 1635), ("ipca_servicos", 10844),
                ("ipca_monitorados", 4449)]
VC05_RESERVA = [("sgs11428", 11428), ("sgs4448", 4448)]
MESES = pd.date_range("2001-01-01", "2025-12-01", freq="MS")


def mensal(codigo):
    s = F.bcb_sgs(codigo, 1996, 2025)
    s.index = s.index.to_period("M").to_timestamp()
    return s[~s.index.duplicated()]


def conferir_codigo(codigo):
    """Conferência numérica do plano: >= 290 meses observados em 2001-2025 e correlação > 0,3 com o IPCA (433)."""
    s = mensal(codigo).reindex(MESES)
    ipca = mensal(433).reindex(MESES)
    n = int(s.notna().sum())
    c = float(s.corr(ipca))
    return dict(codigo=codigo, meses=n, corr_ipca=round(c, 3), ok=bool(n >= 290 and c > 0.3))


@functools.lru_cache(maxsize=1)
def vc05_alvos():
    """Os 4 códigos que passam na conferência, na ordem declarada, completando com a reserva."""
    out = []
    for nome, cod in VC05_CODIGOS + VC05_RESERVA:
        if len(out) == 4:
            break
        if conferir_codigo(cod)["ok"]:
            out.append((nome, cod))
    if len(out) < 4:
        raise RuntimeError("VC05: menos de 4 códigos passam na conferência")
    return out
