"""Usinas eólicas e solares do ONS (Fator de Capacidade, CC-BY), 2024-2025.

A escolha usa só metadados (capacidade, coordenadas, completude dos registros), nunca resultados de previsão.
O processamento dos 24 arquivos mensais é feito uma vez e guardado em dados/ons/ (fora do git).
"""
import functools

import pandas as pd

from lab import fontes as F

ANOS = [2024, 2025]
HORAS = pd.date_range("2024-01-01 00:00", "2025-12-31 23:00", freq="h")
CACHE = F.CACHE / "ons" / "usinas_2024_2025.pkl"


@functools.lru_cache(maxsize=1)
def _tabela():
    if CACHE.exists():
        return pd.read_pickle(CACHE)
    df = F.ons_fator(ANOS)
    df = df[(df["din_instante"] >= HORAS[0]) & (df["din_instante"] <= HORAS[-1])]
    ger = df.pivot_table(index="din_instante", columns="nom_usina_conjunto", values="val_geracaoverificada").reindex(HORAS)
    meta = df.groupby("nom_usina_conjunto").agg(tipo=("nom_tipousina", "first"), cap=("val_capacidadeinstalada", "max"),
                                                lat=("val_latitudesecoletora", "first"),
                                                lon=("val_longitudesecoletora", "first"))
    meta["completude"] = ger.notna().mean().reindex(meta.index)
    out = dict(ger=ger, meta=meta)
    pd.to_pickle(out, CACHE)
    return out


def escolher(tipo, n=6):
    """As n maiores usinas do tipo por capacidade, com coordenadas e >= 95% das horas com geração."""
    m = _tabela()["meta"]
    m = m[(m["tipo"] == tipo) & m["lat"].notna() & m["lon"].notna() & (m["completude"] >= 0.95)]
    m = m.sort_values("cap", ascending=False).head(n)
    return [dict(nome=k, cap=round(float(r.cap), 1), lat=float(r.lat), lon=float(r.lon),
                 completude=round(float(r.completude), 4)) for k, r in m.iterrows()]


def geracao(nome):
    return _tabela()["ger"][nome]
