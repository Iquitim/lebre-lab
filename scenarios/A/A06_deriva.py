"""A06: deriva gradual do coeficiente."""
import numpy as np

from lab.metrics import found
from lab.synth import ar1, lag

T = 30000

SPEC = dict(
    id="A06",
    frente="A",
    pergunta="Quando o efeito de uma entrada muda devagar (inclusive de sinal), a LEBRE acompanha?",
    expectativa="Os pesos da LEBRE se adaptam continuamente (NLMS), então ela deve acompanhar a deriva de forma "
                "parecida com a regressão linear online com esquecimento. Perto dos instantes em que o coeficiente "
                "passa por zero, a entrada pouco ajuda, e a aceitação depende de quando a evidência se acumula.",
    criterio="x0 aceita em pelo menos 16 de 20 séries e MSE da LEBRE relativo ao linear online (média geométrica) "
             "no máximo 1,10.",
    sementes=list(range(601, 621)),
    aquecimento=0.2,
    notas="y = b(t) x0(t-3) + ruído 0,6, com b(t) = cos(2 pi t / 30000) (de 1 a -1 e de volta); x1 irrelevante.",
)


def gerar(semente):
    rng = np.random.default_rng(semente)
    X = ar1(rng, T, 2); b = np.cos(2 * np.pi * np.arange(T) / T)
    y = b * lag(X[:, 0], 3) + 0.6 * rng.standard_normal(T)
    return dict(nome=f"s{semente}", grupo="deriva", y=y, X=X, truth=dict(relevant=["x0"]))


def avaliar(resumo, series):
    n = sum(found(r, "x0") for r in series); resumo["x0_aceita"] = n
    return "atende" if n >= 16 and resumo["mse_rel_linear_online_geo"] <= 1.10 else "nao_atende"
