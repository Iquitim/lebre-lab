"""MODELO DE CENÁRIO (copie para scenarios/<frente>/<ID>_<nome>.py e preencha ANTES de rodar).

Regra: pergunta, expectativa e critério são escritos e commitados antes da execução. Depois de rodar, este arquivo
não é editado; uma versão corrigida vira um novo arquivo (ex.: A02b_...) que cita o anterior nas notas.
"""
import numpy as np

SPEC = dict(
    id="A00",
    frente="A",
    pergunta="O que este cenário quer descobrir, em uma frase.",
    expectativa="O que esperamos que aconteça, e por quê (escrito antes de rodar).",
    criterio="Condição objetiva de sucesso, a mesma implementada em avaliar().",
    sementes=[1, 2, 3, 4, 5],
    aquecimento=0.2,          # fração (ou número de passos) inicial excluída das métricas de previsão
    notas="",
)


def gerar(semente):
    """Uma série por semente. Devolve y (T,), X (T, d) e, se a verdade for conhecida, truth."""
    rng = np.random.default_rng(semente)
    T, d = 5000, 3
    X = rng.standard_normal((T, d))
    y = 0.5 * rng.standard_normal(T)
    return dict(nome=f"s{semente}", y=y, X=X, season=None,
                truth=dict(relevant=[]))           # entradas verdadeiras, ex. ["x0"]


def avaliar(resumo):
    """Aplica o critério ao resumo agregado. Devolve 'atende', 'nao_atende' ou 'inconclusivo'."""
    return "atende" if resumo.get("falsas_aceitas_total", 0) == 0 else "nao_atende"
