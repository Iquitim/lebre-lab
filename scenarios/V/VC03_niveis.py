"""VC03 (validação, análoga a C03, negativa): níveis de preço em 2000-2009 (analises/VALIDACAO_PLANO.md)."""
from lab import validacao as V
from lab.financas import defasar
from lab.real import criterio_nulo, serie

SPEC = dict(id="VC03", frente="V", pergunta="Validação da M2 (análoga a C03).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2, notas="Mesma construção de C03, dias úteis de 2000 a 2009.")


def gerar(i):
    n = V.niveis()
    alvo = V.ATIVOS[i]
    ent = defasar(n[[a for a in V.ATIVOS if a != alvo] + ["juro_2a", "juro_10a"]])
    s = serie(f"nivel_{alvo}_2000_2009", n[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]))
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "ingenuo")
