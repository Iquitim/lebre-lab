"""VB06 (validação, análoga a B06): usinas eólicas de posição 7 a 12 por capacidade (analises/VALIDACAO_PLANO.md)."""
from lab import fontes as F
from lab.real import criterio_padrao, serie, vento_uv
from lab.usinas import escolher, geracao

TIPO = "Eólica"
SPEC = dict(id="VB06", frente="V", pergunta="Validação da M2 (análoga a B06).", expectativa="-", criterio="ver plano",
            sementes=list(range(6)), aquecimento=0.2,
            notas="ONS Fator de Capacidade 2024-2025 (CC-BY); vento ERA5 via Open-Meteo (CC BY 4.0). Posições 7 a 12 do "
                  "mesmo filtro de B06.")


def gerar(i):
    u = escolher(TIPO, n=12)[6 + i]
    t = F.open_meteo(u["lat"], u["lon"], "2024-01-01", "2025-12-31",
                     ["wind_speed_100m", "wind_direction_100m", "wind_speed_10m", "temperature_2m"])
    uu, vv = vento_uv(t["wind_speed_100m"], t["wind_direction_100m"])
    t = t.assign(vento100_u=uu, vento100_v=vv).drop(columns=["wind_direction_100m"])
    return serie(u["nome"], geracao(u["nome"]), t, season=24)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
