"""W-B01 (validação 2, análoga a B01): usinas solares de posição 13 a 18 por capacidade (analises/VALIDACAO2_PLANO.md)."""
from lab import fontes as F
from lab.real import criterio_padrao, serie
from lab.usinas import escolher, geracao

TIPO = "Solar"
VARS = ["shortwave_radiation", "direct_normal_irradiance", "cloud_cover", "temperature_2m"]


def usinas():
    u = escolher(TIPO, n=18)[12:18]
    if len(u) < 3:
        raise RuntimeError("W-B01: menos de 3 usinas a partir da 13ª (família sai, declarar)")
    return u


SPEC = dict(id="W-B01", frente="W", pergunta="Validação 2 da M2 (análoga a B01).", expectativa="-", criterio="ver plano",
            sementes=list(range(6)), aquecimento=0.2,
            notas="ONS Fator de Capacidade 2024-2025 (CC-BY); tempo ERA5 via Open-Meteo (CC BY 4.0).")


def gerar(i):
    u = usinas()[i]
    tempo = F.open_meteo(u["lat"], u["lon"], "2024-01-01", "2025-12-31", VARS)
    return serie(u["nome"], geracao(u["nome"]), tempo, season=24)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
