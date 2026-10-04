"""C04: variação diária dos juros americanos (teste quase negativo)."""
from lab.ativos import JUROS, retornos
from lab.financas import defasar
from lab.real import criterio_nulo, serie

SPEC = dict(
    id="C04",
    frente="C",
    pergunta="Na variação diária dos juros de 3 meses, 2 e 10 anos, a LEBRE encontra algo além do próprio passado, sem "
             "aceitar entradas espúrias?",
    expectativa="As variações diárias de juros longos são quase imprevisíveis. Os juros curtos (3 meses) têm alguma "
                "inércia em torno das decisões do Fed, que a memória da própria série pode captar. Não esperamos entradas "
                "externas aceitas.",
    criterio="Teste negativo: MSE relativo a 'prever zero' (média geométrica) <= 1,02, e no máximo 1 das 3 séries com "
             "alguma entrada externa aceita.",
    sementes=[0, 1, 2],
    aquecimento=0.2,
    notas="2010-2025, dias úteis. Alvos: variação diária (pontos percentuais) dos juros de 3 meses, 2 e 10 anos (Fed "
          "H.15, domínio público). Entradas, com 1 dia de atraso: variações dos outros dois prazos e retornos do "
          "dólar/real, do euro/dólar e do petróleo.",
)


def gerar(i):
    r = retornos(); alvo = f"d_{JUROS[i]}"
    ent = defasar(r[[f"d_{j}" for j in JUROS if f"d_{j}" != alvo] + ["dolar_real", "euro_dolar", "petroleo_wti"]])
    s = serie(alvo, r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
