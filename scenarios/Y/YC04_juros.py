"""Y-C04 (validação 4, análoga a C04, negativa): variação diária dos juros de 1, 5 e 30 anos, 1990-1999."""
from lab import validacao4 as W
from lab.financas import defasar
from lab.real import criterio_nulo, serie

JUROS = list(W.JUROS)
SPEC = dict(id="Y-C04", frente="W", pergunta="Validação 4 da M2 (análoga a C04).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2], aquecimento=0.2, notas="Fed H.15 e H.10 via FRED (domínio público), dias úteis 1990-1999.")


def gerar(i):
    r = W.retornos()
    alvo = f"d_{JUROS[i]}"
    ent = defasar(r[[f"d_{j}" for j in JUROS if f"d_{j}" != alvo] + ["iene_1990", "coroa_dinamarquesa_1990", "dolar_singapura_1990"]])
    s = serie(alvo, r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
