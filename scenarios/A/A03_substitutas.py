"""A03: substitutas correlacionadas."""
import numpy as np

from lab.metrics import found, group_table
from lab.synth import ar1, lag

GRUPOS = {0.5: range(301, 311), 0.8: range(321, 331), 0.95: range(341, 351)}   # correlação -> sementes

SPEC = dict(
    id="A03",
    frente="A",
    pergunta="Quando uma entrada irrelevante é muito correlacionada com a verdadeira, a LEBRE aceita a substituta no "
             "lugar da verdadeira? Com que frequência?",
    expectativa="Com correlação 0,5 ela deve escolher a verdadeira quase sempre. Com 0,95 as duas são quase "
                "indistinguíveis (limitação declarada na pesquisa): a substituta deve ser aceita com frequência, mas "
                "a previsão continua boa, porque alguma das duas entra.",
    criterio="Em todos os grupos, x0 ou x1 aceita em pelo menos 9 de 10 séries; no grupo de correlação 0,5, a "
             "substituta x1 aceita em no máximo 1 de 10.",
    sementes=[s for r in GRUPOS.values() for s in r],
    aquecimento=0.2,
    notas="y = 0,8 x0(t-3) + ruído 0,6; x1 = rho x0 + sqrt(1-rho^2) e (mesmo instante); x2 irrelevante; T = 20000.",
)


def gerar(semente):
    rho = next(k for k, r in GRUPOS.items() if semente in r)
    rng = np.random.default_rng(semente); T = 20000
    x0, x2 = ar1(rng, T, 2).T
    x1 = rho * x0 + np.sqrt(1 - rho ** 2) * ar1(rng, T, 1)[:, 0]
    y = 0.8 * lag(x0, 3) + 0.6 * rng.standard_normal(T)
    return dict(nome=f"rho{rho}_s{semente}", grupo=f"rho{rho}", y=y, X=np.c_[x0, x1, x2], truth=dict(relevant=["x0"]))


def avaliar(resumo, series):
    tab = group_table(series, ["x0", "x1"]); resumo["por_grupo"] = tab
    some = {g: sum(found(r, "x0") or found(r, "x1") for r in series if r["grupo"] == g) for g in tab}
    resumo["alguma_das_duas"] = some
    ok = all(v >= 9 for v in some.values()) and tab["rho0.5"]["aceita_x1"] <= 1
    return "atende" if ok else "nao_atende"
