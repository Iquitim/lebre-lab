"""D05b: teste amplo do protótipo de M2 (porta do D04, sem ajuste). Ver lab/m2.py."""
from lab import m2

ARQUIVOS = ['A/A07_intermitente.py', 'A/A08_faltantes.py', 'A/A09_outliers_sensor_travado.py', 'A/A10_nao_linear.py', 'A/A11_caudas_pesadas.py', 'A/A12_escala.py']
MODS, SERIES = m2.series_de(ARQUIVOS)

SPEC = dict(
    id="D05b",
    frente="D",
    pergunta="A porta do protótipo de M2 (D04) piora a previsão onde a LEBRE já vence a referência trivial, nos cenários "
             "que o D04 não cobriu?",
    expectativa="Onde a vantagem da LEBRE aparece cedo e é grande, a porta deve ficar quase sempre na LEBRE (perda ~0). O "
                "risco está onde a vantagem é pequena ou demora (sintéticos com detecção lenta, eólica): a porta pode ficar "
                "na referência mais tempo e perder um pouco.",
    criterio=m2.CRITERIO,
    sementes=list(range(len(SERIES))),
    aquecimento=0.2,
    notas="Porta idêntica à do D04 (média exponencial da diferença de perda, alfa = 0,01), sem ajuste. Cenários: "
          + ", ".join(ARQUIVOS) + ".",
)


def gerar(i):
    return m2.gerar_com_porta(MODS, SERIES[i])


def avaliar(resumo, series):
    return m2.avaliar(resumo, series)
