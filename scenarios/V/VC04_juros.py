"""VC04 (validação, análoga a C04, negativa): variação diária dos juros americanos em 2000-2009."""
from lab import validacao as V
from lab.financas import defasar
from lab.real import criterio_nulo, serie

SPEC = dict(id="VC04", frente="V", pergunta="Validação da M2 (análoga a C04).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2], aquecimento=0.2, notas="Mesma construção de C04, dias úteis de 2000 a 2009.")


def gerar(i):
    r = V.retornos()
    alvo = f"d_{V.JUROS[i]}"
    ent = defasar(r[[f"d_{j}" for j in V.JUROS if f"d_{j}" != alvo] + ["dolar_real", "euro_dolar", "petroleo_wti"]])
    s = serie(f"{alvo}_2000_2009", r[alvo], ent, freq=None)
    s.update(truth=dict(relevant=[]), zero_baseline=True)
    return s


def avaliar(resumo, series):
    return criterio_nulo(resumo, series, "zero")
