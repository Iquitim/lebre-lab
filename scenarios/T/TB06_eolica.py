"""T-B06 (validação 7, análoga a B06): eólicas a partir da 37ª por capacidade, pulando a reserva da v0.54 e as 6 da
validação 6 (analises/VALIDACAO7_PLANO.md)."""
from lab import fontes as F
from lab.real import criterio_padrao, serie, vento_uv
from lab.reserva import USINAS_V054
from lab.usinas import escolher, geracao

TIPO = "Eólica"


def usinas():
    elegiveis = [x for x in escolher(TIPO, n=200)[36:] if x["nome"] not in USINAS_V054]
    u = elegiveis[6:12]                                             # as 6 primeiras foram da validação 6
    if len(u) < 3:
        raise RuntimeError("T-B06: menos de 3 usinas elegíveis (família sai, declarar)")
    return u


SPEC = dict(id="T-B06", frente="T", pergunta="Validação 7 (análoga a B06).", expectativa="-", criterio="ver plano",
            sementes=list(range(6)), aquecimento=0.2,
            notas="ONS Fator de Capacidade 2024-2025 (CC-BY); vento ERA5 via Open-Meteo (CC BY 4.0); ciclo 24.")


def gerar(i):
    u = usinas()[i]
    t = F.open_meteo(u["lat"], u["lon"], "2024-01-01", "2025-12-31",
                     ["wind_speed_100m", "wind_direction_100m", "wind_speed_10m", "temperature_2m"])
    uu, vv = vento_uv(t["wind_speed_100m"], t["wind_direction_100m"])
    t = t.assign(vento100_u=uu, vento100_v=vv).drop(columns=["wind_direction_100m"])
    return serie(u["nome"], geracao(u["nome"]), t, season=24)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
