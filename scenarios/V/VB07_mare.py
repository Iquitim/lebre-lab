"""VB07 (validação, análoga a B07): maré meteorológica em 6 estações novas da NOAA (analises/VALIDACAO_PLANO.md)."""
import functools

import pandas as pd

from lab import fontes as F
from lab import validacao as V
from lab.real import criterio_padrao, serie, vento_uv

ANOS = [2021, 2022, 2023, 2024]
SPEC = dict(id="VB07", frente="V", pergunta="Validação da M2 (análoga a B07).", expectativa="-", criterio="ver plano",
            sementes=list(range(6)), aquecimento=0.2,
            notas="NOAA CO-OPS 2021-2024 (domínio público), mesma construção de B07; estações e reservas fixadas no plano.")


def _noaa_serie(est, produto, extra):
    d = pd.concat([F.noaa(est, produto, a, extra) for a in ANOS])
    return pd.Series(pd.to_numeric(d["v"], errors="coerce").to_numpy(), index=pd.to_datetime(d["t"]))


def _montar(est, nome, lat, lon):
    alt = _noaa_serie(est, "hourly_height", {"datum": "MSL"})
    prev = _noaa_serie(est, "predictions", {"datum": "MSL", "interval": "h"})
    mare_met = (alt - prev.reindex(alt.index)).rename("mare_meteorologica")
    t = F.open_meteo(lat, lon, f"{ANOS[0]}-01-01", f"{ANOS[-1]}-12-31",
                     ["wind_speed_10m", "wind_direction_10m", "pressure_msl"], fuso="GMT")
    u, v = vento_uv(t["wind_speed_10m"], t["wind_direction_10m"])
    ent = pd.DataFrame({"vento_u": u, "vento_v": v, "pressao": t["pressure_msl"]})
    return serie(f"{est}_{nome}", mare_met, ent)


@functools.lru_cache(maxsize=1)
def estacoes():
    """As 6 estações do plano; uma que não puder ser obtida é trocada pela próxima da reserva, na ordem."""
    out, reserva = [], list(V.ESTACOES_RESERVA)
    for e in V.ESTACOES:
        try:
            _montar(*e)
            out.append(e)
        except RuntimeError as ex:
            print("VB07: estação indisponível, trocada pela reserva:", e[0], ex)
            while reserva:
                r = reserva.pop(0)
                try:
                    _montar(*r)
                    out.append(r)
                    break
                except RuntimeError as ex2:
                    print("VB07: reserva indisponível:", r[0], ex2)
    return out


def gerar(i):
    return _montar(*estacoes()[i])


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "ingenuo")
