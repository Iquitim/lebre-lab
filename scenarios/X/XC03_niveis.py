"""X-C03 (validação 3, análoga a C03, negativa): níveis de 4 câmbios novos (validação 3), 2010-2025."""
from lab import validacao3 as W
from lab.financas import defasar
from lab.real import criterio_nulo, serie

ATIVOS = list(W.CAMBIOS)
SPEC = dict(id="X-C03", frente="W", pergunta="Validação 3 da M2 (análoga a C03).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2, notas="Fed H.10 e H.15 via FRED (domínio público), dias úteis 2010-2025.")


def gerar(i):
    n = W.niveis()
    alvo = ATIVOS[i]
    ent = defasar(n[[a for a in ATIVOS if a != alvo] + ["juro_2a", "juro_10a"]])
    s = serie(f"nivel_{alvo}", n[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]))
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "ingenuo")
