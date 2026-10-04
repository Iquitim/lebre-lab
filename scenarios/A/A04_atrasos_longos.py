"""A04: atrasos longos."""
import numpy as np

from lab.metrics import group_table
from lab.synth import ar1, lag

GRUPOS = {24: range(401, 411), 48: range(421, 431), 96: range(441, 451), 200: range(461, 471)}   # atraso -> sementes

SPEC = dict(
    id="A04",
    frente="A",
    pergunta="Até que atraso a LEBRE descobre o efeito de uma entrada?",
    expectativa="A versão congelada cobre atrasos de 1 a 31 passos (bandas 1, 2-3, 4-7, 8-15, 16-31). Atraso 24 deve "
                "ser descoberto; 48, 96 e 200 não, porque estão fora da faixa e a entrada AR(1) quase não tem "
                "correlação com o próprio passado tão distante. Este teste confirma um limite conhecido.",
    criterio="Atraso 24: x0 aceita em pelo menos 8 de 10 séries. Atrasos 48, 96 e 200: x0 aceita em no máximo 2 de 10. "
             "Em todos os grupos, no máximo 1 série com entrada falsa aceita.",
    sementes=[s for r in GRUPOS.values() for s in r],
    aquecimento=0.2,
    notas="y = 0,8 x0(t-atraso) + ruído 0,6; x1 irrelevante; entradas AR(1) 0,5; T = 20000.",
)


def gerar(semente):
    k = next(a for a, r in GRUPOS.items() if semente in r)
    rng = np.random.default_rng(semente); T = 20000
    X = ar1(rng, T, 2)
    y = 0.8 * lag(X[:, 0], k) + 0.6 * rng.standard_normal(T)
    return dict(nome=f"lag{k}_s{semente}", grupo=f"lag{k}", y=y, X=X, truth=dict(relevant=["x0"]))


def avaliar(resumo, series):
    tab = group_table(series, ["x0"]); resumo["por_grupo"] = tab
    ok = tab["lag24"]["aceita_x0"] >= 8 and all(tab[f"lag{k}"]["aceita_x0"] <= 2 for k in (48, 96, 200)) \
        and all(g["series_com_falsa"] <= 1 for g in tab.values())
    return "atende" if ok else "nao_atende"
