"""C01: retornos diários (teste negativo)."""
from lab.ativos import ATIVOS, retornos
from lab.financas import defasar
from lab.real import criterio_nulo, serie

SPEC = dict(
    id="C01",
    frente="C",
    pergunta="Nos retornos diários de câmbio e petróleo, onde quase nada é previsível, a LEBRE evita aceitar entradas "
             "espúrias e não piora a previsão trivial (retorno zero)?",
    expectativa="O retorno do dia seguinte é praticamente imprevisível com informação pública defasada. Esperamos que a "
                "LEBRE fique perto de 'prever zero' e não aceite entradas externas. Se aceitar alguma, é um sinal de "
                "alerta para uso em finanças.",
    criterio="Teste negativo: MSE relativo a 'prever zero' (média geométrica) <= 1,02, e no máximo 1 das 4 séries com "
             "alguma entrada externa aceita.",
    sementes=[0, 1, 2, 3],
    aquecimento=0.2,
    notas="2010-2025, dias úteis. Alvos: retorno log diário (%) de dólar/real (BCB, ODbL), euro/dólar e iene/dólar (Fed "
          "H.10) e petróleo WTI (EIA), domínio público. Entradas, com 1 dia de atraso: retornos dos outros 3 ativos e "
          "variações dos juros americanos de 2 e 10 anos. Em 20/04/2020 o WTI foi negativo: o retorno log desses dias "
          "fica faltante.",
)


def gerar(i):
    r = retornos(); alvo = ATIVOS[i]
    ent = defasar(r[[a for a in ATIVOS if a != alvo] + ["d_juro_2a", "d_juro_10a"]])
    s = serie(alvo, r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
