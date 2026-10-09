"""Validação 5 da v0.53 (M1 r5 + M2 Q2). Regras: analises/VALIDACAO5_PLANO.md (commitadas antes de qualquer download)."""
import functools
import io
import re
import zipfile

import numpy as np
import pandas as pd

from lab import fontes as F

# ------------------------------------------------------------------ UCI Beijing Multi-Site Air Quality (CC BY 4.0)
URL_PEQUIM = "https://archive.ics.uci.edu/static/public/501/beijing+multi+site+air+quality+data.zip"
POLUENTES = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
METEO = ["TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
ALVOS_PEQUIM = ["PM2.5", "NO2", "CO", "O3"]


def _arquivos_pequim():
    b = F._get(URL_PEQUIM, F.CACHE / "uci_pequim" / "beijing_multi_site.zip")
    z = zipfile.ZipFile(io.BytesIO(b))
    internos = [n for n in z.namelist() if n.startswith("PRSA") and n.lower().endswith(".zip")]
    if internos:                                                    # os dados das estações vêm num zip interno
        z = zipfile.ZipFile(io.BytesIO(z.read(internos[0])))
    csvs = sorted(n for n in z.namelist() if "PRSA_Data_" in n.split("/")[-1] and n.lower().endswith(".csv"))
    return z, csvs


@functools.lru_cache(maxsize=1)
def estacao_pequim():
    """A segunda estação em ordem alfabética (regra do plano): nome e DataFrame horário."""
    z, csvs = _arquivos_pequim()
    nomes = sorted((re.search(r"PRSA_Data_(.+?)_\d", n.split("/")[-1]).group(1), n) for n in csvs)
    nome, arq = nomes[1]
    df = pd.read_csv(z.open(arq))
    df.index = pd.to_datetime(df[["year", "month", "day", "hour"]])
    return nome, df[POLUENTES + METEO].astype(float).asfreq("h")


# ------------------------------------------------------------------ finanças, 2000-2009 (Z-C01 a Z-C04)
DIAS = pd.bdate_range("2000-01-01", "2009-12-31")
CAMBIOS = {"won_2000": "DEXKOUS", "peso_mexicano_2000": "DEXMXUS", "franco_suico_2000": "DEXSZUS",
           "coroa_norueguesa_2000": "DEXNOUS"}
JUROS = {"juro_1a_2000": "DGS1", "juro_5a_2000": "DGS5", "juro_20a_2000": "DGS20"}


def _cal(s):
    return s[~s.index.duplicated()].reindex(DIAS)


@functools.lru_cache(maxsize=1)
def niveis():
    d = {k: _cal(F.fred(v)) for k, v in CAMBIOS.items()}
    d |= {k: _cal(F.fred(v)) for k, v in JUROS.items()}
    d |= {"juro_2a": _cal(F.fred("DGS2")), "juro_10a": _cal(F.fred("DGS10"))}
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


# ------------------------------------------------------------------ NOAA (Z-B07)
ESTACOES = ["8516945", "8729840", "8652587", "9431647", "8557380", "9449880"]
ESTACOES_RESERVA = ["9419750", "8770570"]

# ------------------------------------------------------------------ IPCA via SGS (Z-C05)
W_C05_CODIGOS = [("ipca_nucleo_11427", 11427), ("ipca_nucleo_4467", 4467), ("ipca_comunicacao", 1640),
                 ("ipca_bens_duraveis", 10843)]
W_C05_RESERVA = [("ipca_vestuario", 1638)]


def estacao_meta(est):
    from lab.validacao2 import estacao_meta as m
    return m(est)


@functools.lru_cache(maxsize=1)
def w_c05_alvos():
    from lab.validacao import conferir_codigo
    out = []
    for nome, cod in W_C05_CODIGOS + W_C05_RESERVA:
        if len(out) == 4:
            break
        if conferir_codigo(cod)["ok"]:
            out.append((nome, cod))
    if len(out) < 3:
        raise RuntimeError("Z-C05: menos de 3 códigos passam na conferência")
    return out
