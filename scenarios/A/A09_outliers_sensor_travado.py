"""A09: outliers e sensor travado."""
import numpy as np

from lab.synth import base_truth

T = 20000

SPEC = dict(
    id="A09",
    frente="A",
    pergunta="Outliers no alvo e nas entradas, e um sensor que trava por um tempo, levam a decisões erradas?",
    expectativa="A evidência usa perdas recortadas e as entradas são limitadas, então outliers isolados não devem gerar "
                "aceitações falsas. Enquanto x0 está travado, ela perde informação e a previsão piora nesse trecho, "
                "mas a estrutura não deve se desfazer.",
    criterio="Recall médio >= 0,8 e no máximo 1 de 20 séries com entrada falsa aceita.",
    sementes=list(range(901, 921)),
    aquecimento=0.2,
    notas="Cenário de referência com d = 4. 0,5% dos valores do alvo e de cada entrada viram outliers de +-8 desvios; "
          "x0 fica travado no último valor entre t = 8000 e t = 11000.",
)


def gerar(semente):
    rng = np.random.default_rng(semente)
    X, y = base_truth(rng, T, 4)
    y = y.copy(); X = X.copy(); sy = y.std()
    i = rng.random(T) < 0.005; y[i] += 8 * sy * rng.choice([-1, 1], i.sum())
    for j in range(4):
        i = rng.random(T) < 0.005; X[i, j] += 8 * rng.choice([-1, 1], i.sum())
    X[8000:11000, 0] = X[7999, 0]
    return dict(nome=f"s{semente}", grupo="outliers", y=y, X=X, truth=dict(relevant=["x0", "x1"]))


def avaliar(resumo, series):
    return "atende" if resumo["recall_medio"] >= 0.8 and resumo["series_com_falsa"] <= 1 else "nao_atende"
