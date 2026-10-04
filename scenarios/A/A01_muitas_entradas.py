"""A01: muitas entradas, só 2 relevantes."""
import numpy as np

from lab.metrics import group_table
from lab.synth import base_truth

GRUPOS = {10: range(101, 111), 20: range(201, 211), 50: range(501, 511)}      # d -> sementes

SPEC = dict(
    id="A01",
    frente="A",
    pergunta="Com 10, 20 e 50 entradas, das quais só 2 importam, a LEBRE acha as relevantes sem aceitar falsas? "
             "Quanto custa por passo?",
    expectativa="Ela testa só 2 hipóteses por vez, então com mais candidatas a detecção deve ficar mais lenta, e com "
                "d = 50 pode não achar as duas em 20 mil passos. As falsas devem continuar controladas. O custo por "
                "passo deve crescer aproximadamente em proporção a d.",
    criterio="Em cada grupo (d = 10, 20, 50): recall médio >= 0,8 e no máximo 1 série (de 10) com entrada falsa aceita.",
    sementes=[s for r in GRUPOS.values() for s in r],
    aquecimento=0.2,
    notas="y = 0,7 x0(t-3) + 0,5 x1(t-10) + ruído 0,7; entradas AR(1) com coeficiente 0,5; T = 20000.",
)


def gerar(semente):
    d = next(k for k, r in GRUPOS.items() if semente in r)
    X, y = base_truth(np.random.default_rng(semente), 20000, d)
    return dict(nome=f"d{d}_s{semente}", grupo=f"d{d}", y=y, X=X, truth=dict(relevant=["x0", "x1"]))


def avaliar(resumo, series):
    tab = group_table(series, ["x0", "x1"]); resumo["por_grupo"] = tab
    ok = all(g["recall_medio"] >= 0.8 and g["series_com_falsa"] <= 1 for g in tab.values())
    return "atende" if ok else "nao_atende"
