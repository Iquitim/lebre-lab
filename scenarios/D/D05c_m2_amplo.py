"""D05c: teste amplo do protótipo de M2 (porta do D04, sem ajuste). Ver lab/m2.py."""
from lab import m2

ARQUIVOS = ['B/B03_qualidade_do_ar.py', 'B/B06_eolica.py', 'B/B07_mare_meteorologica.py', 'C/C02_volatilidade.py', 'C/C05_macro_mensal_curta.py']
MODS, SERIES = m2.series_de(ARQUIVOS)

SPEC = dict(
    id="D05c",
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
