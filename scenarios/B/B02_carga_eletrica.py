"""B02: carga elétrica horária dos quatro subsistemas do ONS, com o tempo na capital de referência."""
from lab import fontes as F
from lab.real import criterio_padrao, serie

ANOS = [2022, 2023, 2024, 2025]
SUBSISTEMAS = [("SUDESTE", "Sao Paulo", -23.55, -46.63), ("SUL", "Porto Alegre", -30.03, -51.23),
               ("NORDESTE", "Recife", -8.05, -34.90), ("NORTE", "Belem", -1.46, -48.50)]
VARS = ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "shortwave_radiation", "precipitation"]

SPEC = dict(
    id="B02",
    frente="B",
    pergunta="A LEBRE prevê a carga elétrica horária melhor que os comparadores, e passa a usar o tempo como entrada?",
    expectativa="A carga tem ciclos diário e semanal fortes, que a memória sazonal da LEBRE (season 24 e 168) captura. "
                "A temperatura deve ajudar, sobretudo no Sudeste e no Nordeste (ar-condicionado); a radiação solar pode "
                "reduzir a carga medida (geração distribuída). Feriados não são informados e devem gerar erros pontuais. "
                "Esperamos vencer o sazonal ingênuo com folga e empatar com o linear online.",
    criterio="Critério padrão da Frente B: MSE relativo ao sazonal ingênuo (média geométrica) < 1; MSE relativo ao linear "
             "online <= 1,05; cobertura média do intervalo de 90% entre 0,85 e 0,95.",
    sementes=[0, 1, 2, 3],
    aquecimento=0.2,
    notas="Carga do ONS 2022-2025 (CC-BY), horário de Brasília. Tempo: reanálise ERA5 via Open-Meteo (CC BY 4.0) na "
          "capital de referência de cada subsistema; é o tempo que ocorreu, não uma previsão (resultado otimista).",
)


def gerar(i):
    sub, cid, lat, lon = SUBSISTEMAS[i]
    carga = F.ons_carga(ANOS)[sub]
    tempo = F.open_meteo(lat, lon, f"{ANOS[0]}-01-01", f"{ANOS[-1]}-12-31", VARS)
    return serie(f"{sub}_{cid}", carga, tempo, season=24, season2=168)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
