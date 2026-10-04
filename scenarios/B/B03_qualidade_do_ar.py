"""B03: poluentes medidos por analisadores de referência, com sensores químicos baratos e meteorologia como entradas."""
from lab import fontes as F
from lab.real import criterio_padrao, serie

ALVOS = ["CO(GT)", "NOx(GT)", "NO2(GT)", "C6H6(GT)"]
ENTRADAS = ["PT08.S1(CO)", "PT08.S2(NMHC)", "PT08.S3(NOx)", "PT08.S4(NO2)", "PT08.S5(O3)", "T", "RH", "AH"]

SPEC = dict(
    id="B03",
    frente="B",
    pergunta="Com sensores químicos baratos medindo no mesmo lugar, a LEBRE prevê a próxima hora do poluente de "
             "referência melhor que os comparadores?",
    expectativa="Os sensores respondem aos mesmos poluentes no mesmo instante, e o valor atual das entradas entra no "
                "modelo base da LEBRE sem decisão nenhuma; por isso esperamos poucas mudanças aceitas e ganho grande sobre "
                "o sazonal ingênuo. Os sensores derivam ao longo do ano (conhecido neste conjunto), o que favorece "
                "métodos que se adaptam. Esperamos empatar com o linear online.",
    criterio="Critério padrão da Frente B: MSE relativo ao sazonal ingênuo (média geométrica) < 1; MSE relativo ao linear "
             "online <= 1,05; cobertura média do intervalo de 90% entre 0,85 e 0,95.",
    sementes=[0, 1, 2, 3],
    aquecimento=0.2,
    notas="UCI Air Quality (De Vito 2008, CC BY 4.0): 9.357 horas, mar/2004 a abr/2005, uma cidade italiana; -200 = "
          "faltante. NMHC(GT) não é usado (90% faltante).",
)


def gerar(i):
    df = F.uci_air()
    return serie(ALVOS[i], df[ALVOS[i]], df[ENTRADAS], season=24, season2=168)


def avaliar(resumo, series):
    return criterio_padrao(resumo, series, "sazonal_ingenuo")
