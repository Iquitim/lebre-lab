"""T-B03 (validação 7, análoga a B03): poluentes da quarta estação de Pequim (analises/VALIDACAO7_PLANO.md)."""
from lab import validacao7 as V7
from lab.real import criterio_padrao, serie

SPEC = dict(id="T-B03", frente="T", pergunta="Validação 7 (análoga a B03).", expectativa="-",
            criterio="ver plano", sementes=[0, 1, 2, 3], aquecimento=0.2,
            notas="UCI Beijing Multi-Site Air Quality (Chen, 2017, doi:10.24432/C5RK5G; CC BY 4.0), horária, mar/2013 a "
                  "fev/2017; estação: a quarta em ordem alfabética.")


def gerar(i):
    nome, df = V7.estacao_pequim()
    alvo = V7.ALVOS_PEQUIM[i]
    ent = [p for p in V7.POLUENTES if p != alvo] + V7.METEO
    return serie(f"{nome}_{alvo}", df[alvo], df[ent], season=24, season2=168)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
