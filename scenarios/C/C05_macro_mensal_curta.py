"""C05: inflação mensal (série curta, ~360 pontos)."""
import pandas as pd

from lab import fontes as F
from lab.real import criterio_padrao, serie

ALVOS = [("ipca", 433), ("inpc", 188)]                    # ambos do IBGE, via SGS do BCB

SPEC = dict(
    id="C05",
    frente="C",
    pergunta="Com uma série curta (cerca de 360 meses), a LEBRE ainda prevê a inflação do próximo mês melhor que os "
             "comparadores?",
    expectativa="As decisões da LEBRE exigem pelo menos 100 amostras de evidência e são testadas a cada 10 passos; com "
                "360 pontos, ela deve aceitar pouca coisa ou nada, e a previsão vem quase só da memória e do modelo base. "
                "A inflação mensal é bem persistente, então o ingênuo é difícil de bater. Este cenário mostra o "
                "comportamento perto do limite de dados.",
    criterio="Critério padrão da Frente B, com o ingênuo como referência: MSE relativo ao ingênuo (média geométrica) < 1; "
             "MSE relativo ao linear online <= 1,05; cobertura média do intervalo de 90% entre 0,85 e 0,95.",
    sementes=[0, 1],
    aquecimento=0.2,
    notas="Jan/1996 a dez/2025, mensal. Alvos: IPCA (433) e INPC (188), do IBGE (reuso com citação da fonte), via SGS "
          "do BCB; variação mensal em %. Entradas, com 1 mês de atraso: o outro índice, variação % do dólar médio do "
          "mês (média da PTAX diária, série 1 do BCB, ODbL) e Selic acumulada no mês (4390, BCB, ODbL). season = 12. "
          "O IGP-M (FGV) foi trocado pelo INPC antes de rodar: a licença da FGV não foi conferida.",
)


def _mensal(codigo):
    s = F.bcb_sgs(codigo, 1996, 2025)
    s.index = s.index.to_period("M").to_timestamp()
    return s[~s.index.duplicated()]


def gerar(i):
    nome, cod = ALVOS[i]
    outro = [c for n, c in ALVOS if c != cod][0]
    d = F.bcb_sgs(1, 1996, 2025)
    dolar = d.groupby(d.index.to_period("M")).mean(); dolar.index = dolar.index.to_timestamp()
    ent = pd.DataFrame({"outro_indice": _mensal(outro), "dolar_var": 100 * dolar.pct_change(),
                        "selic_mes": _mensal(4390)}).shift(1)
    alvo = _mensal(cod)
    idx = pd.date_range("1996-01-01", "2025-12-01", freq="MS")
    s = serie(nome, alvo.reindex(idx), ent.reindex(idx), season=12, freq=None)
    return s


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "ingenuo")
