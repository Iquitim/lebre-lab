"""W-B06 (validação 2, análoga a B06): usinas eólicas de posição 13 a 18 por capacidade (analises/VALIDACAO2_PLANO.md)."""
from lab import fontes as F
from lab.real import criterio_padrao, serie, vento_uv
from lab.usinas import escolher, geracao

TIPO = "Eólica"


def usinas():
    u = escolher(TIPO, n=18)[12:18]
    if len(u) < 3:
        raise RuntimeError("W-B06: menos de 3 usinas a partir da 13ª (família sai, declarar)")
    return u


SPEC = dict(id="W-B06", frente="W", pergunta="Validação 2 da M2 (análoga a B06).", expectativa="-", criterio="ver plano",
            sementes=list(range(6)), aquecimento=0.2,
            notas="ONS Fator de Capacidade 2024-2025 (CC-BY); vento ERA5 via Open-Meteo (CC BY 4.0).")


def gerar(i):
    u = usinas()[i]
    t = F.open_meteo(u["lat"], u["lon"], "2024-01-01", "2025-12-31",
                     ["wind_speed_100m", "wind_direction_100m", "wind_speed_10m", "temperature_2m"])
    uu, vv = vento_uv(t["wind_speed_100m"], t["wind_direction_100m"])
    t = t.assign(vento100_u=uu, vento100_v=vv).drop(columns=["wind_direction_100m"])
    return serie(u["nome"], geracao(u["nome"]), t, season=24)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
