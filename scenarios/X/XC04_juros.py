"""X-C04 (validação 3, análoga a C04, negativa): variação diária dos juros de 3, 7 e 20 anos, 2010-2025."""
from lab import validacao3 as W
from lab.financas import defasar
from lab.real import criterio_nulo, serie

JUROS = list(W.JUROS)
SPEC = dict(id="X-C04", frente="W", pergunta="Validação 3 da M2 (análoga a C04).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2], aquecimento=0.2, notas="Fed H.15 e H.10 via FRED (domínio público), dias úteis 2010-2025.")


def gerar(i):
    r = W.retornos()
    alvo = f"d_{JUROS[i]}"
    ent = defasar(r[[f"d_{j}" for j in JUROS if f"d_{j}" != alvo] + ["ringgit", "dolar_taiwan", "rupia_sri_lanka"]])
    s = serie(alvo, r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
