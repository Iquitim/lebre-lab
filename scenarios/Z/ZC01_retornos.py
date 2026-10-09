"""Z-C01 (validação 5, análoga a C01, negativa): retornos diários de 4 câmbios novos (validação 5), 2000-2009."""
from lab import validacao5 as W
from lab.financas import defasar
from lab.real import criterio_nulo, serie

ATIVOS = list(W.CAMBIOS)
SPEC = dict(id="Z-C01", frente="W", pergunta="Validação 5 da M2 (análoga a C01).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2, notas="Fed H.10 via FRED (domínio público), dias úteis 2000-2009.")


def gerar(i):
    r = W.retornos()
    alvo = ATIVOS[i]
    ent = defasar(r[[a for a in ATIVOS if a != alvo] + ["d_juro_2a", "d_juro_10a"]])
    s = serie(alvo, r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
