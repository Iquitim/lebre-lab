"""A12: escala (série longa com muitas entradas)."""
import numpy as np

from lab.synth import base_truth

SPEC = dict(
    id="A12",
    frente="A",
    pergunta="Numa série de 200 mil passos com 50 entradas, quanto custa cada passo e a LEBRE se mantém estável?",
    expectativa="O custo analítico cresce com d (somas de bandas e o modelo base usam todas as entradas), mas deve "
                "ficar abaixo de 3 mil operações por passo. O tempo real depende desta máquina e do Python; o "
                "relevante é a ordem de grandeza.",
    criterio="Termina, sem previsões não finitas depois do aquecimento, com custo médio <= 3000 operações por passo e "
             "tempo real <= 2000 microssegundos por passo (Python, nesta máquina).",
    sementes=[1201],
    aquecimento=0.2,
    notas="Cenário de referência com d = 50 e T = 200000. Tempo real medido só no laço da LEBRE.",
)


def gerar(semente):
    X, y = base_truth(np.random.default_rng(semente), 200000, 50)
    return dict(nome=f"s{semente}", grupo="escala", y=y, X=X, truth=dict(relevant=["x0", "x1"]))


def avaliar(resumo, series):
    r = series[0]
    resumo.update(us_por_passo=r["us_por_passo"], previsoes_nao_finitas=r["previsoes_nao_finitas"])
    ok = r["previsoes_nao_finitas"] == 0 and r["custo_medio"] <= 3000 and r["us_por_passo"] <= 2000
    return "atende" if ok else "nao_atende"
