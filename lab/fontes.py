"""Carregadores de dados reais (Frente B). Cada fonte é baixada uma vez para dados/ (fora do git) e lida de lá.

Licenças e atribuições: dados/FONTES.md (conferidas antes de qualquer download).
"""
import io
import json
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "dados"
UA = {"User-Agent": "lebre-lab (pesquisa sem fins comerciais; github.com/Iquitim/lebre)"}


def _get(url, path, tries=4):
    """Baixa url para path (uma vez). Devolve os bytes."""
    path = Path(path)
    if path.exists():
        return path.read_bytes()
    path.parent.mkdir(parents=True, exist_ok=True)
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                b = r.read()
            path.write_bytes(b)
            return b
        except Exception as ex:                                   # noqa: BLE001
            if k == tries - 1:
                raise RuntimeError(f"falhou: {url}: {ex}") from ex
            time.sleep(5 * (k + 1))


# ------------------------------------------------------------------ UCI Air Quality (CC BY 4.0)
def uci_air():
    """DataFrame horário com as colunas originais; -200 vira NaN; índice = data e hora local."""
    b = _get("https://archive.ics.uci.edu/static/public/360/air+quality.zip", CACHE / "uci_air" / "air+quality.zip")
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        df = pd.read_csv(z.open("AirQualityUCI.csv"), sep=";", decimal=",")
    df = df.dropna(how="all", axis=1).dropna(subset=["Date"])
    df.index = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H.%M.%S")
    df = df.drop(columns=["Date", "Time"]).astype(float).replace(-200.0, np.nan)
    return df.asfreq("h")


# ------------------------------------------------------------------ ONS (CC-BY)
def _ons_resources(dataset):
    url = f"https://dados.ons.org.br/api/3/action/package_show?id={dataset}"
    meta = json.loads(_get(url, CACHE / "ons" / f"{dataset}.json"))
    return meta["result"]["resources"]


def ons_csvs(dataset, keep):
    """Lê e concatena os CSVs de um conjunto do ONS cujo nome satisfaz keep(nome)."""
    out = []
    for r in _ons_resources(dataset):
        if r["format"].upper() == "CSV" and keep(r["name"]):
            fn = r["url"].rsplit("/", 1)[-1]
            b = _get(r["url"], CACHE / "ons" / dataset / fn)
            out.append(pd.read_csv(io.BytesIO(b), sep=";", decimal="."))
    return pd.concat(out, ignore_index=True)


def ons_carga(anos):
    """Carga horária por subsistema (MWmed), horário local de Brasília."""
    from lab.reserva import checar_data
    checar_data(f"{max(anos)}-12-31", "carga do ONS")
    df = ons_csvs("curva-carga", lambda n: any(str(a) in n for a in anos))
    df["din_instante"] = pd.to_datetime(df["din_instante"])
    return df.pivot_table(index="din_instante", columns="nom_subsistema", values="val_cargaenergiahomwmed")


def ons_fator(anos):
    """Geração horária verificada por usina eólica/solar, com capacidade e coordenadas."""
    df = ons_csvs("fator-capacidade-2", lambda n: any(f"{a}" in n for a in anos))
    df["din_instante"] = pd.to_datetime(df["din_instante"])
    return df


# ------------------------------------------------------------------ Open-Meteo, reanálise histórica (CC BY 4.0)
def open_meteo(lat, lon, inicio, fim, variaveis, fuso="America/Sao_Paulo"):
    """Série horária de reanálise (ERA5) num ponto. inicio/fim: 'AAAA-MM-DD'."""
    from lab.reserva import checar_data
    checar_data(fim, "meteorologia")
    q = dict(latitude=f"{lat:.4f}", longitude=f"{lon:.4f}", start_date=inicio, end_date=fim,
             hourly=",".join(variaveis), timezone=fuso)
    url = "https://archive-api.open-meteo.com/v1/archive?" + urllib.parse.urlencode(q)
    fn = f"{lat:.4f}_{lon:.4f}_{inicio}_{fim}_{'-'.join(variaveis)}_{fuso.replace('/', '-')}.json"
    d = json.loads(_get(url, CACHE / "open_meteo" / fn))["hourly"]
    return pd.DataFrame({k: d[k] for k in variaveis}, index=pd.to_datetime(d["time"])).astype(float)


# ------------------------------------------------------------------ NOAA CO-OPS (domínio público)
def noaa(estacao, produto, ano, extra=None):
    """Um ano de um produto horário de uma estação NOAA (UTC, unidades métricas)."""
    q = dict(product=produto, application="lebre-lab", begin_date=f"{ano}0101", end_date=f"{ano}1231",
             station=estacao, time_zone="gmt", units="metric", format="json", **(extra or {}))
    url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?" + urllib.parse.urlencode(q)
    d = json.loads(_get(url, CACHE / "noaa" / f"{estacao}_{produto}_{ano}.json"))
    key = "predictions" if produto == "predictions" else "data"
    if key not in d:
        raise RuntimeError(f"NOAA {estacao} {produto} {ano}: {str(d)[:200]}")
    return pd.DataFrame(d[key])


# ------------------------------------------------------------------ Banco Central do Brasil, SGS (ODbL)
def bcb_sgs(codigo, inicio, fim):
    """Série do SGS entre os anos inicio e fim (inclusive), em blocos de até 10 anos (limite do API para séries diárias)."""
    partes = []
    for a in range(inicio, fim + 1, 10):
        b = min(a + 9, fim)
        q = dict(formato="json", dataInicial=f"01/01/{a}", dataFinal=f"31/12/{b}")
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?" + urllib.parse.urlencode(q)
        arq = CACHE / "bcb" / f"sgs{codigo}_{a}_{b}.json"
        for k in range(3):                                    # o SGS às vezes devolve uma página de erro HTML
            try:
                d = json.loads(_get(url, arq))
                break
            except json.JSONDecodeError:
                arq.unlink(missing_ok=True)
                if k == 2:
                    raise
                time.sleep(5 * (k + 1))
        partes.append(pd.DataFrame(d))
    df = pd.concat(partes)
    return pd.Series(pd.to_numeric(df["valor"], errors="coerce").to_numpy(),
                     index=pd.to_datetime(df["data"], format="%d/%m/%Y"), name=f"sgs{codigo}").sort_index()


# ------------------------------------------------------------------ FRED: só séries de domínio público (dados/FONTES.md)
FRED_DOMINIO_PUBLICO = {"DGS10", "DGS2", "DTB3", "DEXUSEU", "DEXJPUS", "DCOILWTICO",
                        # validação 2 da v0.53 (status conferido em 08/10/2026, dados/FONTES.md)
                        "DEXINUS", "DEXSIUS", "DEXTHUS", "DEXDNUS", "DGS1", "DGS5", "DGS30",
                        # validação 3 da v0.53 (status conferido em 08/10/2026, dados/FONTES.md)
                        "DEXMAUS", "DEXTAUS", "DEXSLUS", "DEXSFUS", "DGS3", "DGS7", "DGS20"}


def fred(serie):
    """Série diária do FRED (download do CSV público). Recusa séries fora da lista de domínio público conferida."""
    from lab.reserva import checar_fred
    checar_fred(serie)
    if serie not in FRED_DOMINIO_PUBLICO:
        raise ValueError(f"{serie}: licença não conferida (dados/FONTES.md)")
    b = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={serie}", CACHE / "fred" / f"{serie}.csv")
    df = pd.read_csv(io.BytesIO(b))
    return pd.Series(pd.to_numeric(df.iloc[:, 1], errors="coerce").to_numpy(), index=pd.to_datetime(df.iloc[:, 0]),
                     name=serie).sort_index()
