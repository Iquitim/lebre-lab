"""Teste amplo do protótipo de M2 (porta do D04, sem nenhum ajuste) em cenários que o D04 não cobriu.

Referência trivial por série: zero quando o cenário a declara (zero_baseline), sazonal ingênuo quando há ciclo,
ingênuo (persistência) nos demais.
"""
import numpy as np

from lab.baselines import Naive, SeasonalNaive, Zero
from lab.ensembles import LebreW, Porta
from lab.run import ROOT, load

CRITERIO = ("Em toda família (cenário) em que a LEBRE vence a referência trivial (MSE da LEBRE ÷ MSE da referência, média "
            "geométrica, < 1), MSE da porta ÷ MSE da LEBRE (média geométrica) <= 1,02. Nas famílias em que a LEBRE perde "
            "para a referência, MSE da porta ÷ MSE da referência é só reportado.")


def series_de(arquivos):
    mods = {a: load(ROOT / "scenarios" / a) for a in arquivos}
    return mods, [(a, s) for a, m in mods.items() for s in m.SPEC["sementes"]]


def gerar_com_porta(mods, item):
    arq, sd = item
    s = mods[arq].gerar(sd)
    season, season2, zero = s.get("season"), s.get("season2"), s.get("zero_baseline")

    def ref(dd):
        return Zero(dd) if zero else (SeasonalNaive(dd, season) if season else Naive(dd))

    s.update(grupo=mods[arq].SPEC["id"], extras=[lambda dd: Porta([LebreW(dd, season=season, season2=season2), ref(dd)],
                                                                   "m2_porta")])
    return s


def _geo(v):
    v = np.asarray(v, float); v = v[np.isfinite(v) & (v > 0)]
    return float(np.exp(np.mean(np.log(v)))) if len(v) else float("nan")


def _ref(r):
    c = r["comparadores"]
    return c["zero"]["mse"] if "zero" in c else (c["sazonal_ingenuo"]["mse"] if "sazonal_ingenuo" in c else c["ingenuo"]["mse"])


def avaliar(resumo, series):
    tab, ok = {}, True
    for g in sorted({r["grupo"] for r in series}):
        rs = [r for r in series if r["grupo"] == g]
        lebre_ref = _geo([r["lebre"]["mse"] / _ref(r) for r in rs])
        porta_lebre = _geo([r["extras"]["m2_porta"]["mse_rel_lebre"] for r in rs])
        porta_ref = _geo([r["extras"]["m2_porta"]["mse"] / _ref(r) for r in rs])
        tab[g] = dict(n=len(rs), lebre_rel_ref=round(lebre_ref, 4), porta_rel_lebre=round(porta_lebre, 4),
                      porta_rel_ref=round(porta_ref, 4), lebre_vence=bool(lebre_ref < 1))
        if lebre_ref < 1 and porta_lebre > 1.02:
            ok = False
    resumo["por_familia"] = tab
    return "atende" if ok else "nao_atende"
