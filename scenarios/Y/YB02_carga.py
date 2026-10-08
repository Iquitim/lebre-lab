"""Y-B02 (validação 4, análoga a B02): carga dos 4 subsistemas do ONS em 2006-2009 (analises/VALIDACAO4_PLANO.md)."""
from lab import fontes as F
from lab.real import criterio_padrao, serie

ANOS = [2006, 2007, 2008, 2009]
SUBSISTEMAS = [("SUDESTE", "Sao Paulo", -23.55, -46.63), ("SUL", "Porto Alegre", -30.03, -51.23),
               ("NORDESTE", "Recife", -8.05, -34.90), ("NORTE", "Belem", -1.46, -48.50)]
VARS = ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "shortwave_radiation", "precipitation"]
SPEC = dict(id="Y-B02", frente="W", pergunta="Validação 4 da M2 (análoga a B02).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2,
            notas="Carga do ONS 2006-2009 (CC-BY); tempo ERA5 via Open-Meteo (CC BY 4.0). Mesma construção de B02.")


def gerar(i):
    sub, cid, lat, lon = SUBSISTEMAS[i]
    carga = F.ons_carga(ANOS)[sub]
    tempo = F.open_meteo(lat, lon, f"{ANOS[0]}-01-01", f"{ANOS[-1]}-12-31", VARS)
    return serie(f"{sub}_{cid}_2006_2009", carga, tempo, season=30, season2=168)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
