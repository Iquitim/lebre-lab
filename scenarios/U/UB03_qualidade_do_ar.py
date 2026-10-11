"""U-B03 (validação 6, análoga a B03): poluentes da terceira estação de Pequim (analises/VALIDACAO6_PLANO.md)."""
from lab import validacao6 as V6
from lab.real import criterio_padrao, serie

SPEC = dict(id="U-B03", frente="U", pergunta="Validação 6 da M5a (análoga a B03, F6).", expectativa="-",
            criterio="ver plano", sementes=[0, 1, 2, 3], aquecimento=0.2,
            notas="UCI Beijing Multi-Site Air Quality (Chen, 2017, doi:10.24432/C5RK5G; CC BY 4.0), horária, mar/2013 a "
                  "fev/2017; estação: a terceira em ordem alfabética.")


def gerar(i):
    nome, df = V6.estacao_pequim()
    alvo = V6.ALVOS_PEQUIM[i]
    ent = [p for p in V6.POLUENTES if p != alvo] + V6.METEO
    return serie(f"{nome}_{alvo}", df[alvo], df[ent], season=24, season2=168)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
