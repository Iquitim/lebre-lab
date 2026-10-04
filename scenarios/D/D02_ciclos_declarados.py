"""D02: ensemble de LEBREs com ciclos declarados diferentes (dados de B02 e B01)."""
from pathlib import Path

import numpy as np

from lab.ensembles import LebreW, Media, PesosOnline
from lab.run import load

ROOT = Path(__file__).resolve().parents[2]
B02 = load(ROOT / "scenarios" / "B" / "B02_carga_eletrica.py")
B01 = load(ROOT / "scenarios" / "B" / "B01_solar.py")
SERIES = [("B02", i) for i in range(4)] + [("B01", i) for i in range(6)]
CICLOS = [(None, None), (12, None), (24, None), (24, 168)]

SPEC = dict(
    id="D02",
    frente="D",
    pergunta="Quando não se sabe qual é o ciclo dos dados, combinar LEBREs com ciclos diferentes chega perto de uma LEBRE "
             "que declara o ciclo certo?",
    expectativa="A LEBRE com o ciclo certo deve ser a melhor. O ensemble deve ficar entre ela e a LEBRE sem ciclo: a "
                "média dilui o membro certo, e os pesos online devem concentrar nele com o tempo. Custo cerca de 4 vezes "
                "o da LEBRE simples.",
    criterio="A hipótese é aceita se o ensemble por pesos tiver erro no máximo 5% acima do da LEBRE com o ciclo certo e "
             "abaixo do da LEBRE sem ciclo (razões de MSE, média geométrica sobre as 10 séries).",
    sementes=list(range(len(SERIES))),
    aquecimento=0.2,
    notas="Séries de B02 (carga, ciclo certo 24 + 168) e B01 (solar, ciclo certo 24). A LEBRE principal de cada série usa "
          "o ciclo certo (como em B01/B02). Membros: sem ciclo, 12, 24, 24 + 168.",
)


def gerar(i):
    cen, k = SERIES[i]
    s = (B02 if cen == "B02" else B01).gerar(k)

    def membros(dd):
        return [LebreW(dd, season=a, season2=b, name=f"ciclo_{a}_{b}") for a, b in CICLOS]

    s.update(grupo=cen, extras=[lambda dd: LebreW(dd, name="lebre_sem_ciclo"),
                                lambda dd: Media(membros(dd), "ens_media"),
                                lambda dd: PesosOnline(membros(dd), "ens_pesos")])
    return s


def _geo(v):
    v = np.asarray(v, float); v = v[np.isfinite(v) & (v > 0)]
    return float(np.exp(np.mean(np.log(v)))) if len(v) else float("nan")


def avaliar(resumo, series):
    out = {}
    for k in ("ens_media", "ens_pesos", "lebre_sem_ciclo"):
        out[k] = dict(mse_rel_lebre_ciclo_certo=_geo([r["extras"][k]["mse_rel_lebre"] for r in series]),
                      custo_rel_lebre=float(np.mean([r["extras"][k]["custo_rel_lebre"] for r in series])))
    for k in ("ens_media", "ens_pesos"):
        out[k]["mse_rel_lebre_sem_ciclo"] = _geo([r["extras"][k]["mse"] / r["extras"]["lebre_sem_ciclo"]["mse"] for r in series])
    resumo["ensembles"] = out
    e = out["ens_pesos"]
    return "atende" if e["mse_rel_lebre_ciclo_certo"] <= 1.05 and e["mse_rel_lebre_sem_ciclo"] < 1 else "nao_atende"
