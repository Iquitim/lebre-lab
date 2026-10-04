"""A10: relações não lineares."""
import numpy as np

from lab.metrics import group_table
from lab.synth import ar1, lag

GRUPOS = {"limiar": range(1001, 1011), "saturacao": range(1021, 1031), "quadratico": range(1041, 1051)}

SPEC = dict(
    id="A10",
    frente="A",
    pergunta="Quando a relação não é linear, a LEBRE ainda encontra a entrada? Quanto perde?",
    expectativa="A LEBRE é linear. Limiar (max(0, x)) e saturação (tanh) têm um componente linear forte, então a "
                "entrada deve ser encontrada. Na relação quadrática simétrica (x^2) a correlação linear é zero: ela deve "
                "ficar cega para o efeito, assim como o linear online. Este teste mostra um limite estrutural.",
    criterio="Limiar e saturação: x0 aceita em pelo menos 8 de 10. Quadrático: x0 aceita em no máximo 2 de 10. Em "
             "todos os grupos, no máximo 1 série com entrada falsa aceita.",
    sementes=[s for r in GRUPOS.values() for s in r],
    aquecimento=0.2,
    notas="x0 atrasado de 3 passos; limiar: 1,2 max(0, x0) + ruído 0,5; saturação: tanh(2 x0) + ruído 0,3; quadrático: "
          "0,7 (x0^2 - 1) + ruído 0,5; x1 e x2 irrelevantes; T = 20000.",
)


def gerar(semente):
    g = next(k for k, r in GRUPOS.items() if semente in r)
    rng = np.random.default_rng(semente); T = 20000
    X = ar1(rng, T, 3); z = lag(X[:, 0], 3)
    if g == "limiar":
        y = 1.2 * np.maximum(0, z) + 0.5 * rng.standard_normal(T)
    elif g == "saturacao":
        y = np.tanh(2 * z) + 0.3 * rng.standard_normal(T)
    else:
        y = 0.7 * (z ** 2 - 1) + 0.5 * rng.standard_normal(T)
    return dict(nome=f"{g}_s{semente}", grupo=g, y=y, X=X, truth=dict(relevant=["x0"]))


def avaliar(resumo, series):
    tab = group_table(series, ["x0"]); resumo["por_grupo"] = tab
    ok = tab["limiar"]["aceita_x0"] >= 8 and tab["saturacao"]["aceita_x0"] >= 8 and tab["quadratico"]["aceita_x0"] <= 2 \
        and all(g["series_com_falsa"] <= 1 for g in tab.values())
    return "atende" if ok else "nao_atende"
