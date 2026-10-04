"""B07: maré meteorológica (nível medido menos maré astronômica prevista), com vento e pressão como entradas."""
import pandas as pd

from lab import fontes as F
from lab.real import criterio_padrao, serie, vento_uv

ANOS = [2021, 2022, 2023, 2024]
ESTACOES = [("8518750", "The Battery NY", 40.7006, -74.0142), ("8443970", "Boston", 42.3539, -71.0503),
            ("8534720", "Atlantic City", 39.3550, -74.4183), ("8665530", "Charleston", 32.7808, -79.9236),
            ("8771450", "Galveston", 29.3100, -94.7933), ("8724580", "Key West", 24.5508, -81.8081)]

SPEC = dict(
    id="B07",
    frente="B",
    pergunta="A LEBRE prevê a próxima hora da maré meteorológica melhor que a persistência, e passa a usar vento e "
             "pressão?",
    expectativa="A maré meteorológica muda devagar, então a persistência (ingênuo) é um comparador forte. Vento ao longo "
                "da costa e pressão afetam o nível com atrasos de algumas horas, dentro da faixa da LEBRE: esperamos que "
                "ela aceite componentes do vento ou a pressão e vença o ingênuo por pouco. Restos da maré astronômica "
                "(período de 12,42 h, não inteiro) não são capturados por uma memória sazonal inteira.",
    criterio="Critério padrão da Frente B com o ingênuo como referência: MSE relativo ao ingênuo (média geométrica) < 1; "
             "MSE relativo ao linear online <= 1,05; cobertura média do intervalo de 90% entre 0,85 e 0,95.",
    sementes=[0, 1, 2, 3, 4, 5],
    aquecimento=0.2,
    notas="NOAA CO-OPS 2021-2024 (domínio público): altura horária verificada menos maré prevista, datum MSL, UTC. Vento a "
          "10 m (u, v) e pressão ao nível do mar: reanálise ERA5 via Open-Meteo (CC BY 4.0) nas coordenadas da estação.",
)


def _noaa_serie(est, produto, extra):
    d = pd.concat([F.noaa(est, produto, a, extra) for a in ANOS])
    return pd.Series(pd.to_numeric(d["v"], errors="coerce").to_numpy(), index=pd.to_datetime(d["t"]))


def gerar(i):
    est, nome, lat, lon = ESTACOES[i]
    alt = _noaa_serie(est, "hourly_height", {"datum": "MSL"})
    prev = _noaa_serie(est, "predictions", {"datum": "MSL", "interval": "h"})
    mare_met = (alt - prev.reindex(alt.index)).rename("mare_meteorologica")
    t = F.open_meteo(lat, lon, f"{ANOS[0]}-01-01", f"{ANOS[-1]}-12-31",
                     ["wind_speed_10m", "wind_direction_10m", "pressure_msl"], fuso="GMT")
    u, v = vento_uv(t["wind_speed_10m"], t["wind_direction_10m"])
    ent = pd.DataFrame({"vento_u": u, "vento_v": v, "pressao": t["pressure_msl"]})
    return serie(f"{est}_{nome}", mare_met, ent)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "ingenuo")
