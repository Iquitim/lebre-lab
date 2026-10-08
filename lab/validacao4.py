"""Validação 4 da v0.53 (M1 com M2). Regras: analises/VALIDACAO4_PLANO.md (commitadas antes de qualquer download)."""
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
    csvs = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
    if not csvs:                                                    # zip dentro do zip (formato da UCI)
        internos = [n for n in z.namelist() if n.lower().endswith(".zip")]
        z = zipfile.ZipFile(io.BytesIO(z.read(internos[0])))
        csvs = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
    return z, csvs


@functools.lru_cache(maxsize=1)
def estacao_pequim():
    """A primeira estação em ordem alfabética (regra do plano): nome e DataFrame horário."""
    z, csvs = _arquivos_pequim()
    nomes = sorted((re.search(r"PRSA_Data_(.+?)_\d", n.split("/")[-1]).group(1), n) for n in csvs)
    nome, arq = nomes[0]
    df = pd.read_csv(z.open(arq))
    df.index = pd.to_datetime(df[["year", "month", "day", "hour"]])
    return nome, df[POLUENTES + METEO].astype(float).asfreq("h")


# ------------------------------------------------------------------ finanças, 1990-1999 (Y-C01 a Y-C04)
DIAS = pd.bdate_range("1990-01-01", "1999-12-31")
CAMBIOS = {"iene_1990": "DEXJPUS", "coroa_dinamarquesa_1990": "DEXDNUS", "dolar_singapura_1990": "DEXSIUS",
           "baht_1990": "DEXTHUS"}
JUROS = {"juro_1a_1990": "DGS1", "juro_5a_1990": "DGS5", "juro_30a_1990": "DGS30"}


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


# ------------------------------------------------------------------ NOAA (Y-B07)
ESTACOES = ["8410140", "8413320", "8418150", "8531680", "8575512", "9415020"]
ESTACOES_RESERVA = ["8652587", "9431647"]

# ------------------------------------------------------------------ núcleos do IPCA via SGS (Y-C05)
W_C05_CODIGOS = [("ipca_nucleo_4466", 4466), ("ipca_nucleo_11426", 11426), ("ipca_nucleo_16121", 16121),
                 ("ipca_nucleo_16122", 16122)]
W_C05_RESERVA = [("ipca_nucleo_11427", 11427), ("ipca_nucleo_4467", 4467)]


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
        raise RuntimeError("Y-C05: menos de 3 códigos passam na conferência")
    return out
