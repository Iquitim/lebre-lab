"""A11: ruído de cauda pesada e ruído heterocedástico."""
import numpy as np

from lab.metrics import group_table
from lab.synth import ar1, lag

GRUPOS = {"t2.5": range(1101, 1121), "hetero": range(1131, 1151)}

SPEC = dict(
    id="A11",
    frente="A",
    pergunta="Com ruído de cauda pesada, ou com a variância dependendo de uma entrada irrelevante para a média, o "
             "controle de mudanças falsas se mantém?",
    expectativa="A evidência usa perdas recortadas, pensadas para caudas pesadas, então as falsas devem continuar "
                "raras. No grupo heterocedástico, x4 muda a variância mas não a média: aceitá-la seria falso, e não "
                "esperamos isso.",
    criterio="Em cada grupo: no máximo 2 de 20 séries com entrada falsa aceita e recall médio >= 0,8.",
    sementes=[s for r in GRUPOS.values() for s in r],
    aquecimento=0.2,
    notas="y = 0,7 x0(t-3) + 0,5 x1(t-10) + ruído; t2.5: ruído t de Student com 2,5 graus de liberdade, desvio 0,7; "
          "hetero: ruído normal com desvio 0,3 + 0,6 |x4(t)|; d = 5; T = 20000.",
)


def gerar(semente):
    g = next(k for k, r in GRUPOS.items() if semente in r)
    rng = np.random.default_rng(semente); T = 20000
    X = ar1(rng, T, 5)
    if g == "t2.5":
        e = 0.7 * rng.standard_t(2.5, T) / np.sqrt(2.5 / 0.5)
    else:
        e = (0.3 + 0.6 * np.abs(X[:, 4])) * rng.standard_normal(T)
    y = 0.7 * lag(X[:, 0], 3) + 0.5 * lag(X[:, 1], 10) + e
    return dict(nome=f"{g}_s{semente}", grupo=g, y=y, X=X, truth=dict(relevant=["x0", "x1"]))


def avaliar(resumo, series):
    tab = group_table(series, ["x0", "x1", "x4"]); resumo["por_grupo"] = tab
    ok = all(g["series_com_falsa"] <= 2 and g["recall_medio"] >= 0.8 for g in tab.values())
    return "atende" if ok else "nao_atende"
