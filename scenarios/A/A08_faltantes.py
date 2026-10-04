"""A08: dados faltando em blocos (alvo e entradas)."""
import numpy as np

from lab.synth import base_truth

T = 20000

SPEC = dict(
    id="A08",
    frente="A",
    pergunta="Com o alvo e as entradas faltando em blocos, a LEBRE continua prevendo e decidindo bem?",
    expectativa="Ela foi feita para alvos faltantes (só não aprende nesses passos) e preenche entradas faltantes com o "
                "último valor. A detecção deve ficar um pouco mais lenta, sem entradas falsas e sem previsões "
                "inválidas.",
    criterio="Recall médio >= 0,8; no máximo 1 de 20 séries com entrada falsa aceita; nenhuma previsão não finita "
             "depois do aquecimento.",
    sementes=list(range(801, 821)),
    aquecimento=0.2,
    notas="Cenário de referência com d = 4. Alvo faltando em blocos de 50 a 500 passos (~15% do total); cada entrada "
          "faltando em blocos de 20 a 200 passos (~5%).",
)


def _blocks(rng, T, frac, lo, hi):
    m = np.zeros(T, bool)
    while m.mean() < frac:
        s = rng.integers(0, T); m[s:s + rng.integers(lo, hi)] = True
    return m


def gerar(semente):
    rng = np.random.default_rng(semente)
    X, y = base_truth(rng, T, 4)
    y = y.copy(); y[_blocks(rng, T, 0.15, 50, 500)] = np.nan
    X = X.copy()
    for j in range(4):
        X[_blocks(rng, T, 0.05, 20, 200), j] = np.nan
    return dict(nome=f"s{semente}", grupo="faltantes", y=y, X=X, truth=dict(relevant=["x0", "x1"]))


def avaliar(resumo, series):
    nf = sum(r["previsoes_nao_finitas"] for r in series); resumo["previsoes_nao_finitas_total"] = nf
    ok = resumo["recall_medio"] >= 0.8 and resumo["series_com_falsa"] <= 1 and nf == 0
    return "atende" if ok else "nao_atende"
