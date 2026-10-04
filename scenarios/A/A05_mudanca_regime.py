"""A05: mudança de regime abrupta (a entrada relevante troca no meio da série)."""
import numpy as np

from lab.metrics import accept_time, found
from lab.synth import ar1, lag

T, TROCA = 30000, 15000

SPEC = dict(
    id="A05",
    frente="A",
    pergunta="Quando a entrada relevante troca no meio da série, a LEBRE aceita a nova a tempo? Remove a antiga?",
    expectativa="A nova (x1) deve ser aceita alguns milhares de passos depois da troca, porque a evidência precisa se "
                "acumular. A antiga (x0) provavelmente NÃO será removida: na pesquisa nenhuma remoção chegou a ser "
                "aceita (a margem de remoção é lenta). O peso de x0 ainda pode ir a zero pela adaptação contínua.",
    criterio="x0 aceita antes da troca em pelo menos 16 de 20 séries, e x1 aceita entre a troca e 8 mil passos depois "
             "em pelo menos 14 de 20.",
    sementes=list(range(501, 521)),
    aquecimento=0.2,
    notas="y = 0,8 x0(t-3) até t = 15000, depois 0,8 x1(t-5); ruído 0,6; x2 irrelevante; T = 30000.",
)


def gerar(semente):
    rng = np.random.default_rng(semente)
    X = ar1(rng, T, 3); on = np.arange(T) < TROCA
    y = np.where(on, 0.8 * lag(X[:, 0], 3), 0.8 * lag(X[:, 1], 5)) + 0.6 * rng.standard_normal(T)
    return dict(nome=f"s{semente}", grupo="troca", y=y, X=X, truth=dict(relevant=["x0", "x1"]))


def avaliar(resumo, series):
    t0 = [accept_time(r, "x0") for r in series]; t1 = [accept_time(r, "x1") for r in series]
    antes = sum(t is not None and t < TROCA for t in t0)
    depois = sum(t is not None and TROCA <= t < TROCA + 8000 for t in t1)
    rem = sum(any(e["resultado"] == "accepted" and e["sai"] and e["sai"].startswith("x0") for e in r["eventos"])
              for r in series)
    resumo.update(x0_antes_da_troca=antes, x1_ate_8mil_depois=depois, x0_removida=rem,
                  atraso_mediano_x1=float(np.median([t - TROCA for t in t1 if t is not None and t >= TROCA]))
                  if any(t is not None and t >= TROCA for t in t1) else None,
                  x1_aceita_alguma_vez=sum(found(r, "x1") for r in series))
    return "atende" if antes >= 16 and depois >= 14 else "nao_atende"
