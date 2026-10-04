"""D03: LEBRE + linear online + sazonal ingênuo (ou ingênuo), com pesos online (todas as séries reais da Frente B)."""
from pathlib import Path

import numpy as np

from lab.baselines import Naive, OnlineLinear, SeasonalNaive
from lab.ensembles import LebreW, PesosOnline
from lab.run import load

ROOT = Path(__file__).resolve().parents[2]
CEN = {c: load(ROOT / "scenarios" / "B" / f) for c, f in [("B01", "B01_solar.py"), ("B02", "B02_carga_eletrica.py"),
                                                           ("B03", "B03_qualidade_do_ar.py"), ("B06", "B06_eolica.py"),
                                                           ("B07", "B07_mare_meteorologica.py")]}
SERIES = [(c, i) for c, m in CEN.items() for i in m.SPEC["sementes"]]

SPEC = dict(
    id="D03",
    frente="D",
    pergunta="Combinar a LEBRE com o linear online e o ingênuo sazonal, com pesos ajustados pelo erro recente, supera o "
             "melhor dos três sozinho em cada série?",
    expectativa="Os pesos online devem seguir o melhor membro, então o ganho mais claro deve aparecer onde a LEBRE perde "
                "(qualidade do ar, F6): lá a combinação deve ficar perto do linear online. Onde a LEBRE já é a melhor, a "
                "combinação deve empatar ou ganhar pouco. Em média, esperamos ficar perto do melhor membro, não muito "
                "abaixo dele.",
    criterio="A hipótese de que a combinação supera o melhor membro é aceita se o MSE da combinação dividido pelo do "
             "melhor membro de cada série (LEBRE, linear online ou ingênuo de referência; média geométrica sobre as 26 "
             "séries) for menor que 1.",
    sementes=list(range(len(SERIES))),
    aquecimento=0.2,
    notas="As 26 séries reais de B01, B02, B03, B06 e B07, montadas como nos cenários originais. Referência ingênua: "
          "sazonal ingênuo quando a série declara ciclo, ingênuo nas marés (B07). O custo dos comparadores não é "
          "contado (só o da LEBRE).",
)


def gerar(i):
    cen, k = SERIES[i]
    s = CEN[cen].gerar(k)
    season, season2 = s.get("season"), s.get("season2")

    def comb(dd):
        ref = SeasonalNaive(dd, season) if season else Naive(dd)
        return PesosOnline([LebreW(dd, season=season, season2=season2), OnlineLinear(dd), ref], "comb_pesos")

    s.update(grupo=cen, extras=[comb])
    return s


def _geo(v):
    v = np.asarray(v, float); v = v[np.isfinite(v) & (v > 0)]
    return float(np.exp(np.mean(np.log(v)))) if len(v) else float("nan")


def avaliar(resumo, series):
    rel_best, rel_lebre, por = [], [], {}
    for r in series:
        ref = "sazonal_ingenuo" if "sazonal_ingenuo" in r["comparadores"] else "ingenuo"
        best = min(r["lebre"]["mse"], r["comparadores"]["linear_online"]["mse"], r["comparadores"][ref]["mse"])
        c = r["extras"]["comb_pesos"]["mse"]
        rel_best.append(c / best); rel_lebre.append(c / r["lebre"]["mse"])
        por.setdefault(r["grupo"], []).append((c / best, c / r["lebre"]["mse"]))
    resumo["comb_rel_melhor_membro_geo"] = _geo(rel_best)
    resumo["comb_rel_lebre_geo"] = _geo(rel_lebre)
    resumo["por_cenario"] = {g: dict(rel_melhor=_geo([a for a, _ in v]), rel_lebre=_geo([b for _, b in v])) for g, v in por.items()}
    return "atende" if resumo["comb_rel_melhor_membro_geo"] < 1 else "nao_atende"
