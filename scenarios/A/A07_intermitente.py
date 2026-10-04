"""A07: efeito intermitente (liga e desliga em blocos)."""
import numpy as np

from lab.metrics import found
from lab.synth import ar1, lag

T, BLOCO = 30000, 5000

SPEC = dict(
    id="A07",
    frente="A",
    pergunta="Quando o efeito de uma entrada liga e desliga em blocos, a LEBRE entra e sai na hora certa, ou oscila?",
    expectativa="Ela deve aceitar x0 num dos primeiros blocos ativos e, sem remoções aceitas, mantê-la depois. Nos "
                "blocos desligados o peso deve ir a zero pela adaptação. Não esperamos oscilação (muitas aceitações "
                "e remoções seguidas).",
    criterio="x0 aceita em pelo menos 16 de 20 séries, MSE relativo ao linear online (média geométrica) no máximo 1,10, "
             "e no máximo 3 eventos aceitos por série em média.",
    sementes=list(range(701, 721)),
    aquecimento=0.2,
    notas="y = 0,9 x0(t-3) nos blocos pares de 5000 passos, 0 nos ímpares, + ruído 0,6; x1 irrelevante; T = 30000.",
)


def gerar(semente):
    rng = np.random.default_rng(semente)
    X = ar1(rng, T, 2); on = (np.arange(T) // BLOCO) % 2 == 0
    y = np.where(on, 0.9 * lag(X[:, 0], 3), 0.0) + 0.6 * rng.standard_normal(T)
    return dict(nome=f"s{semente}", grupo="intermitente", y=y, X=X, truth=dict(relevant=["x0"]))


def avaliar(resumo, series):
    n = sum(found(r, "x0") for r in series)
    ev = float(np.mean([sum(e["resultado"] == "accepted" for e in r["eventos"]) for r in series]))
    resumo.update(x0_aceita=n, eventos_aceitos_por_serie=ev)
    ok = n >= 16 and resumo["mse_rel_linear_online_geo"] <= 1.10 and ev <= 3
    return "atende" if ok else "nao_atende"
