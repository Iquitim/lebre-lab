"""Y-B03 (validação 4, análoga a B03): poluentes de uma estação de Pequim, com os outros poluentes e a meteorologia
no mesmo instante como entradas (analises/VALIDACAO4_PLANO.md)."""
from lab import validacao4 as V4
from lab.real import criterio_padrao, serie

SPEC = dict(id="Y-B03", frente="Y", pergunta="Validação 4 da M1 (análoga a B03, F6).", expectativa="-",
            criterio="ver plano", sementes=[0, 1, 2, 3], aquecimento=0.2,
            notas="UCI Beijing Multi-Site Air Quality (Chen, 2017, doi:10.24432/C5RK5G; CC BY 4.0), horária, mar/2013 a "
                  "fev/2017; estação: a primeira em ordem alfabética.")


def gerar(i):
    nome, df = V4.estacao_pequim()
    alvo = V4.ALVOS_PEQUIM[i]
    ent = [p for p in V4.POLUENTES if p != alvo] + V4.METEO
    return serie(f"{nome}_{alvo}", df[alvo], df[ent], season=24, season2=168)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
