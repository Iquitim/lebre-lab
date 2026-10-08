"""Y-C02 (validação 4, análoga a C02): volatilidade realizada diária de 4 câmbios novos (validação 4), 1990-1999."""
from lab import validacao4 as W
from lab.financas import defasar
from lab.real import criterio_padrao, serie

ATIVOS = list(W.CAMBIOS)
SPEC = dict(id="Y-C02", frente="W", pergunta="Validação 4 da M2 (análoga a C02).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2, notas="Fed H.10 via FRED (domínio público), dias úteis 1990-1999.")


def gerar(i):
    r = W.retornos().abs()
    alvo = ATIVOS[i]
    ent = defasar(r[[a for a in ATIVOS if a != alvo] + ["d_juro_2a", "d_juro_10a"]])
    return serie(f"abs_{alvo}", r[alvo], ent, freq=None)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "ingenuo")
