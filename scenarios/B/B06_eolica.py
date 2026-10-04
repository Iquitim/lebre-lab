"""B06: geração eólica horária das maiores usinas do ONS, com o vento no local da usina."""
from lab import fontes as F
from lab.real import criterio_padrao, serie, vento_uv
from lab.usinas import escolher, geracao

TIPO = "Eólica"

SPEC = dict(
    id="B06",
    frente="B",
    pergunta="A LEBRE prevê a geração eólica da próxima hora melhor que os comparadores, usando o vento no local?",
    expectativa="A geração eólica é muito persistente de uma hora para a outra, então o sazonal ingênuo é um "
                "comparador fraco e o ganho sobre ele deve ser grande; o teste relevante é o empate com o linear "
                "online. A relação com a velocidade do vento é não linear (curva de potência, próxima do cubo até a "
                "velocidade nominal), o que limita uma relação linear (ver A10).",
    criterio="Critério padrão da Frente B: MSE relativo ao sazonal ingênuo (média geométrica) < 1; MSE relativo ao linear "
             "online <= 1,05; cobertura média do intervalo de 90% entre 0,85 e 0,95.",
    sementes=list(range(6)),
    aquecimento=0.2,
    notas="ONS Fator de Capacidade 2024-2025 (CC-BY): geração verificada (MWmed). Usinas escolhidas só por metadados: as "
          "6 maiores por capacidade, com coordenadas e >= 95% das horas com geração. Vento a 100 m (velocidade, u, v), "
          "vento a 10 m e temperatura: reanálise ERA5 via Open-Meteo (CC BY 4.0); é o tempo que ocorreu, não previsão.",
)


def gerar(i):
    u = escolher(TIPO)[i]
    t = F.open_meteo(u["lat"], u["lon"], "2024-01-01", "2025-12-31",
                     ["wind_speed_100m", "wind_direction_100m", "wind_speed_10m", "temperature_2m"])
    uu, vv = vento_uv(t["wind_speed_100m"], t["wind_direction_100m"])
    t = t.assign(vento100_u=uu, vento100_v=vv).drop(columns=["wind_direction_100m"])
    return serie(u["nome"], geracao(u["nome"]), t, season=24)


def avaliar(resumo, series):
    resumo["usinas"] = escolher(TIPO)
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
