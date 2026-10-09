"""Z-C04 (validação 5, análoga a C04, negativa): variação diária dos juros de 1, 5 e 20 anos, 2000-2009."""
from lab import validacao5 as W
from lab.financas import defasar
from lab.real import criterio_nulo, serie

JUROS = list(W.JUROS)
SPEC = dict(id="Z-C04", frente="W", pergunta="Validação 5 da M2 (análoga a C04).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2], aquecimento=0.2, notas="Fed H.15 e H.10 via FRED (domínio público), dias úteis 2000-2009.")


def gerar(i):
    r = W.retornos()
    alvo = f"d_{JUROS[i]}"
    ent = defasar(r[[f"d_{j}" for j in JUROS if f"d_{j}" != alvo] + ["won_2000", "peso_mexicano_2000", "franco_suico_2000"]])
    s = serie(alvo, r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
