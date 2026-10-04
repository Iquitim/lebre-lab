"""A02: cenário nulo, só entradas irrelevantes."""
import numpy as np

from lab.synth import ar1

SPEC = dict(
    id="A02",
    frente="A",
    pergunta="Quando nenhuma entrada ajuda a prever, quantas mudanças falsas a LEBRE aceita?",
    expectativa="Poucas ou nenhuma: na pesquisa, 0 de 400 simulações nulas tiveram mudança falsa. O alvo tem dinâmica "
                "própria (AR(1)), então aceitar o próprio passado é legítimo e não conta como falsa.",
    criterio="No máximo 2 das 40 séries (5%) com alguma entrada falsa aceita.",
    sementes=list(range(1, 41)),
    aquecimento=0.2,
    notas="5 entradas AR(1) independentes do alvo; y AR(1) com coeficiente 0,6 e ruído 1; T = 20000.",
)


def gerar(semente):
    rng = np.random.default_rng(semente); T = 20000
    X = ar1(rng, T, 5)
    e = rng.standard_normal(T); y = np.empty(T); y[0] = e[0]
    for t in range(1, T):
        y[t] = 0.6 * y[t - 1] + e[t]
    return dict(nome=f"s{semente}", grupo="nulo", y=y, X=X, truth=dict(relevant=[]))


def avaliar(resumo, series):
    return "atende" if resumo["series_com_falsa"] <= 2 else "nao_atende"
