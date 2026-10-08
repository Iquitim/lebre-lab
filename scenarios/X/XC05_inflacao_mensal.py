"""X-C05 (validação 3, análoga a C05): classificações do IPCA, variação mensal 2001-2025 (analises/VALIDACAO3_PLANO.md)."""
import pandas as pd

from lab import fontes as F
from lab import validacao as V
from lab import validacao3 as W
from lab.real import criterio_padrao, serie

SPEC = dict(id="X-C05", frente="W", pergunta="Validação 3 da M2 (análoga a C05).", expectativa="-", criterio="ver plano",
            sementes=[0, 1, 2, 3], aquecimento=0.2,
            notas="IBGE via SGS do BCB. Entradas com 1 mês de atraso: IPCA cheio (433), variação do dólar médio do mês (1) "
                  "e Selic do mês (4390). season = 12.")


def gerar(i):
    nome, cod = W.w_c05_alvos()[i]
    d = F.bcb_sgs(1, 1996, 2025)
    dolar = d.groupby(d.index.to_period("M")).mean()
    dolar.index = dolar.index.to_timestamp()
    ent = pd.DataFrame({"ipca": V.mensal(433), "dolar_var": 100 * dolar.pct_change(),
                        "selic_mes": V.mensal(4390)}).shift(1)
    return serie(nome, V.mensal(cod).reindex(V.MESES), ent.reindex(V.MESES), season=12, freq=None)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "ingenuo")
