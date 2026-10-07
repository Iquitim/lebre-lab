"""VC01 (validação, análoga a C01, negativa): retornos diários em 2000-2009 (analises/VALIDACAO_PLANO.md)."""
from lab import validacao as V
from lab.financas import defasar
from lab.real import criterio_nulo, serie

SPEC = dict(id="VC01", frente="V", pergunta="Validação da M2 (análoga a C01).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2, notas="Mesma construção de C01, dias úteis de 2000 a 2009.")


def gerar(i):
    r = V.retornos()
    alvo = V.ATIVOS[i]
    ent = defasar(r[[a for a in V.ATIVOS if a != alvo] + ["d_juro_2a", "d_juro_10a"]])
    s = serie(f"{alvo}_2000_2009", r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
