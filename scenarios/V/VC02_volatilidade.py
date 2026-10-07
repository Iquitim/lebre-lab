"""VC02 (validação, análoga a C02): volatilidade realizada diária em 2000-2009 (analises/VALIDACAO_PLANO.md)."""
from lab import validacao as V
from lab.financas import defasar
from lab.real import criterio_padrao, serie

SPEC = dict(id="VC02", frente="V", pergunta="Validação da M2 (análoga a C02).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2, notas="Mesma construção de C02, dias úteis de 2000 a 2009.")


def gerar(i):
    r = V.retornos().abs()
    alvo = V.ATIVOS[i]
    ent = defasar(r[[a for a in V.ATIVOS if a != alvo] + ["d_juro_2a", "d_juro_10a"]])
    return serie(f"abs_{alvo}_2000_2009", r[alvo], ent, freq=None)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "ingenuo")
