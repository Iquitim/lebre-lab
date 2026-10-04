"""B01: geração solar horária das maiores usinas do ONS, com o tempo no local da usina."""
from lab import fontes as F
from lab.real import criterio_padrao, serie
from lab.usinas import escolher, geracao

TIPO = "Solar"
VARS = ["shortwave_radiation", "direct_normal_irradiance", "cloud_cover", "temperature_2m"]

SPEC = dict(
    id="B01",
    frente="B",
    pergunta="A LEBRE prevê a geração solar da próxima hora melhor que os comparadores, usando o tempo no local?",
    expectativa="A geração solar segue o ciclo do dia (memória sazonal de 24 h) e a irradiância do mesmo instante, que "
                "entra no modelo base sem decisão. Nuvens explicam o que o ciclo não explica. A relação é quase linear "
                "na irradiância, com corte na capacidade máxima (limiar, que a LEBRE trata razoavelmente segundo A10). "
                "Esperamos vencer o sazonal ingênuo com folga e empatar com o linear online.",
    criterio="Critério padrão da Frente B: MSE relativo ao sazonal ingênuo (média geométrica) < 1; MSE relativo ao linear "
             "online <= 1,05; cobertura média do intervalo de 90% entre 0,85 e 0,95.",
    sementes=list(range(6)),
    aquecimento=0.2,
    notas="ONS Fator de Capacidade 2024-2025 (CC-BY): geração verificada (MWmed). Usinas escolhidas só por metadados: as "
          "6 maiores por capacidade, com coordenadas e >= 95% das horas com geração. Tempo: reanálise ERA5 via "
          "Open-Meteo (CC BY 4.0) nas coordenadas; é o tempo que ocorreu, não previsão (resultado otimista). Geração "
          "programada não é usada.",
)


def gerar(i):
    u = escolher(TIPO)[i]
    tempo = F.open_meteo(u["lat"], u["lon"], "2024-01-01", "2025-12-31", VARS)
    return serie(u["nome"], geracao(u["nome"]), tempo, season=24)


def avaliar(resumo, series):
    resumo["usinas"] = escolher(TIPO)
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
