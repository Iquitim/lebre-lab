"""VB01 (validação, análoga a B01): usinas solares de posição 7 a 12 por capacidade (analises/VALIDACAO_PLANO.md)."""
from lab import fontes as F
from lab.real import criterio_padrao, serie
from lab.usinas import escolher, geracao

TIPO = "Solar"
VARS = ["shortwave_radiation", "direct_normal_irradiance", "cloud_cover", "temperature_2m"]
SPEC = dict(id="VB01", frente="V", pergunta="Validação da M2 (análoga a B01).", expectativa="-", criterio="ver plano",
            sementes=list(range(6)), aquecimento=0.2,
            notas="ONS Fator de Capacidade 2024-2025 (CC-BY); tempo ERA5 via Open-Meteo (CC BY 4.0). Posições 7 a 12 do "
                  "mesmo filtro de B01.")


def gerar(i):
    u = escolher(TIPO, n=12)[6 + i]
    tempo = F.open_meteo(u["lat"], u["lon"], "2024-01-01", "2025-12-31", VARS)
    return serie(u["nome"], geracao(u["nome"]), tempo, season=24)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
