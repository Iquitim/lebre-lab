"""E14 (plano: diagnosticos/E14_PLANO.md): fronteira precisão × custo nas famílias onde o comparador completo vence a
v0.52. Só descrição. Uso: python -m diagnosticos.e14_fronteira FAM ...  |  --resumo"""
import json
import math
import sys
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from analises.m1_val4_alvo import Completo8
from diagnosticos.e13_comum import series
from diagnosticos.f6_e10 import BANDAS, RLSBandas, fp
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics

FAMILIAS = ["B03", "B07", "VB07", "VC05", "XB07", "YB03", "YB06", "A05"]
SAIDA = Path(__file__).with_name("e14")


def familia(fam):
    res = []
    for s in series(fam):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape; ini = int(0.2 * T)
        m52 = M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), porta=False)
        f52 = M.rodar(m52, X, y)
        comp = forecast_metrics(y, M.rodar_ref(OnlineLinear(d), X, y), ini)["mse"]
        ok = np.isfinite(y[:ini])
        r = np.array([abs(np.corrcoef(np.nan_to_num(X[:ini][ok, j]), y[:ini][ok])[0, 1]) for j in range(d)])
        top3 = np.argsort(-np.nan_to_num(r))[:3]
        v = {"v0.52": (forecast_metrics(y, f52, ini)["mse"] / comp, m52.cost_per_step)}
        for nome, usa, bandas in (("AR2+0", np.arange(d), [(0, 0)]), ("AR2+B3", top3, BANDAS),
                                  ("AR2+B-todas", np.arange(d), BANDAS)):
            for cada in (1, 8):
                m = RLSBandas(usa, bandas, cada)
                v[f"{nome}/{cada}"] = (forecast_metrics(y, M.rodar_ref(m, X, y), ini)["mse"] / comp, fp(m.k, len(usa), cada))
        k = 3 + 9 * d
        v["COMPLETO/1"] = (1.0, fp(k, 0, 1))
        v["COMPLETO/8"] = (forecast_metrics(y, M.rodar_ref(Completo8(d), X, y), ini)["mse"] / comp, fp(k, 0, 8))
        res.append(dict(serie=s["nome"], d=d, v=v))
        print(fam, s["nome"], {a: round(b[0], 3) for a, b in v.items()}, flush=True)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def resumo():
    L = ["# Diagnóstico E14: a v0.52 na fronteira precisão × custo (resultado)", "",
         "Plano `E14_PLANO.md`. Erro = MSE ÷ comparador linear online completo (média geométrica da família); custo em FP por "
         "passo (média). e* = menor erro entre as variantes com custo <= o da v0.52; e*(2,5) = idem com custo <= 2,5 vezes.", "",
         "| Família | séries | d | v0.52 (erro @ custo) | e* (variante) | v0.52 ÷ e* | e*(2,5) (variante) | v0.52 ÷ e*(2,5) | classificação |",
         "|---|---|---|---|---|---|---|---|---|"]
    for fam in FAMILIAS:
        p = SAIDA / f"{fam}.json"
        if not p.exists():
            continue
        R = json.loads(p.read_text(encoding="utf-8"))
        nomes = list(R[0]["v"])
        geo = {n: math.exp(np.mean([math.log(x["v"][n][0]) for x in R])) for n in nomes}
        cus = {n: float(np.mean([x["v"][n][1] for x in R])) for n in nomes}
        c = cus["v0.52"]
        def melhor(lim):
            cand = [(geo[n], n) for n in nomes if n != "v0.52" and cus[n] <= lim]
            return min(cand) if cand else (math.nan, "-")
        e1, n1 = melhor(c); e2, n2 = melhor(2.5 * c)
        cl = "abaixo" if geo["v0.52"] > 1.05 * e1 else "na fronteira"
        L.append(f"| {fam} | {len(R)} | {R[0]['d']} | {geo['v0.52']:.3f} @ {c:.0f} | {e1:.3f} ({n1}, {cus.get(n1, math.nan):.0f}) | "
                 f"{geo['v0.52'] / e1:.3f} | {e2:.3f} ({n2}, {cus.get(n2, math.nan):.0f}) | {geo['v0.52'] / e2:.3f} | {cl} |")
    Path(__file__).with_name("E14_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
