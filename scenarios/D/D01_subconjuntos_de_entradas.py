"""D01: ensemble de LEBREs, cada uma vendo um subconjunto sorteado das entradas (dados de A01)."""
import numpy as np

from lab.ensembles import LebreW, Media, PesosOnline
from lab.synth import base_truth

GRUPOS = {20: range(2001, 2011), 50: range(5001, 5011)}      # d -> sementes
K = 5                                                         # membros

SPEC = dict(
    id="D01",
    frente="D",
    pergunta="Cinco LEBREs, cada uma vendo metade das entradas (sorteadas), combinadas pela média ou por pesos online, "
             "erram menos que uma LEBRE vendo todas? Quanto custa?",
    expectativa="Provavelmente não ajuda: em A01 a LEBRE sozinha já achou as 2 entradas certas em todas as séries. Cada "
                "membro vê x0 com chance 1/2 e as duas com chance ~1/4, então vários membros ficam sem informação e "
                "puxam a média para pior. Os pesos online devem compensar em parte. O custo total deve ficar perto de "
                "K/2 = 2,5 vezes o da LEBRE simples, porque o custo cresce com o número de entradas.",
    criterio="A hipótese de que ajuda é aceita se, nos dois grupos (d = 20 e d = 50), o erro do ensemble por média e o "
             "do ensemble por pesos ficarem abaixo do da LEBRE simples (razão de MSE, média geométrica < 1).",
    sementes=[s for r in GRUPOS.values() for s in r],
    aquecimento=0.2,
    notas="Dados idênticos aos de A01 (y = 0,7 x0(t-3) + 0,5 x1(t-10) + ruído; entradas AR(1)); T = 20000. Subconjuntos "
          "de tamanho d/2 sorteados por membro com semente derivada da série.",
)


def gerar(semente):
    d = next(k for k, r in GRUPOS.items() if semente in r)
    X, y = base_truth(np.random.default_rng(semente), 20000, d)
    rng = np.random.default_rng(semente + 999)
    subs = [sorted(rng.choice(d, d // 2, replace=False).tolist()) for _ in range(K)]

    def membros(dd):
        return [LebreW(dd, cols=c, name=f"m{j}") for j, c in enumerate(subs)]

    return dict(nome=f"d{d}_s{semente}", grupo=f"d{d}", y=y, X=X, truth=dict(relevant=["x0", "x1"]),
                subconjuntos=subs, extras=[lambda dd: Media(membros(dd), "ens_media"),
                                           lambda dd: PesosOnline(membros(dd), "ens_pesos")])


def _geo(v):
    v = np.asarray(v, float); v = v[np.isfinite(v) & (v > 0)]
    return float(np.exp(np.mean(np.log(v)))) if len(v) else float("nan")


def avaliar(resumo, series):
    tab = {}
    for g in sorted({r["grupo"] for r in series}):
        rs = [r for r in series if r["grupo"] == g]
        tab[g] = {k: dict(mse_rel_lebre=_geo([r["extras"][k]["mse_rel_lebre"] for r in rs]),
                          custo_rel_lebre=float(np.mean([r["extras"][k]["custo_rel_lebre"] for r in rs])))
                  for k in ("ens_media", "ens_pesos")}
    resumo["por_grupo"] = tab
    ok = all(v["mse_rel_lebre"] < 1 for g in tab.values() for v in g.values())
    return "atende" if ok else "nao_atende"
