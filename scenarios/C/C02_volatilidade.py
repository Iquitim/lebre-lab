"""C02: volatilidade realizada diária (estrutura conhecida: agrupamento e contágio entre mercados)."""
from lab.ativos import ATIVOS, retornos
from lab.financas import defasar
from lab.real import criterio_padrao, serie

SPEC = dict(
    id="C02",
    frente="C",
    pergunta="Na volatilidade diária, onde há estrutura conhecida (dias agitados vêm em sequência e se espalham entre "
             "mercados), a LEBRE aproveita essa estrutura?",
    expectativa="O tamanho do retorno de hoje (|r|) depende do de ontem e dos dias anteriores (agrupamento de "
                "volatilidade) e da agitação em outros mercados. A memória da LEBRE deve capturar parte disso e vencer a "
                "persistência simples, que é muito ruidosa. O |r| é assimétrico (nunca negativo), então a cobertura do "
                "intervalo simétrico pode ficar fora da faixa.",
    criterio="Critério padrão da Frente B, com a persistência (ingênuo) como referência: MSE relativo ao ingênuo (média "
             "geométrica) < 1; MSE relativo ao linear online <= 1,05; cobertura média do intervalo de 90% entre 0,85 e "
             "0,95.",
    sementes=[0, 1, 2, 3],
    aquecimento=0.2,
    notas="2010-2025, dias úteis. Alvo: |retorno log diário| (%) de cada ativo de C01. Entradas, com 1 dia de atraso: "
          "|retorno| dos outros 3 ativos e |variação| dos juros de 2 e 10 anos.",
)


def gerar(i):
    r = retornos().abs(); alvo = ATIVOS[i]
    ent = defasar(r[[a for a in ATIVOS if a != alvo] + ["d_juro_2a", "d_juro_10a"]])
    return serie(f"abs_{alvo}", r[alvo], ent, freq=None)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "ingenuo")
