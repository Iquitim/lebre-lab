"""C03: níveis de preço (passeio aleatório e risco de regressão espúria)."""
from lab.ativos import ATIVOS, niveis
from lab.financas import defasar
from lab.real import criterio_nulo, serie

SPEC = dict(
    id="C03",
    frente="C",
    pergunta="Prevendo o nível do câmbio e do petróleo (não o retorno), a LEBRE bate o passeio aleatório? Ela cai na "
             "armadilha da regressão espúria entre séries que andam sem rumo?",
    expectativa="Níveis de câmbio se comportam quase como passeio aleatório: a melhor previsão é o valor de ontem, e a "
                "memória da LEBRE deve chegar perto disso. Séries não estacionárias parecem correlacionadas por acaso "
                "(regressão espúria); o teste estatístico dela pode ser enganado por isso, e este cenário mede se é.",
    criterio="Teste negativo: MSE relativo ao ingênuo (passeio aleatório; média geométrica) <= 1,02, e no máximo 1 das 4 "
             "séries com alguma entrada externa aceita.",
    sementes=[0, 1, 2, 3],
    aquecimento=0.2,
    notas="2010-2025, dias úteis. Alvos: nível de dólar/real, euro/dólar, iene/dólar e petróleo WTI. Entradas, com 1 dia "
          "de atraso: níveis dos outros 3 ativos e dos juros americanos de 2 e 10 anos.",
)


def gerar(i):
    n = niveis(); alvo = ATIVOS[i]
    ent = defasar(n[[a for a in ATIVOS if a != alvo] + ["juro_2a", "juro_10a"]])
    s = serie(f"nivel_{alvo}", n[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]))
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "ingenuo")
