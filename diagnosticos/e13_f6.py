"""E13, parte C (plano: diagnosticos/E13_PLANO.md): v0.52 ÷ comparador linear online completo em todas as famílias
gastas. Só descrição. Uso: python -m diagnosticos.e13_f6 FAM ...  |  --resumo"""
import json
import math
import sys
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from diagnosticos.e13_comum import ARQ, series
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics

SAIDA = Path(__file__).with_name("e13_f6")


def familia(fam):
    res = []
    for s in series(fam):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape; ini = int(0.2 * T)
        f52 = M.rodar(M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), porta=False), X, y)
        fl = M.rodar_ref(OnlineLinear(d), X, y)
        a, b = forecast_metrics(y, f52, ini)["mse"], forecast_metrics(y, fl, ini)["mse"]
        res.append(dict(serie=s["nome"], d=d, T=T, v052_sobre_linear=a / b))
        print(fam, s["nome"], d, round(a / b, 3), flush=True)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def resumo():
    L = ["# E13, parte C: v0.52 ÷ comparador linear online completo, por família", "",
         "Média geométrica por família (> 1: o comparador é melhor). Só descrição, dados já gastos.", "",
         "| Família | séries | d | geo | mín | máx |", "|---|---|---|---|---|---|"]
    for fam in ARQ:
        p = SAIDA / f"{fam}.json"
        if not p.exists():
            continue
        r = [x for x in json.loads(p.read_text(encoding="utf-8")) if math.isfinite(x["v052_sobre_linear"])]
        v = [x["v052_sobre_linear"] for x in r]
        if not v:
            continue
        L.append(f"| {fam} | {len(v)} | {r[0]['d']} | {math.exp(np.mean(np.log(v))):.3f} | {min(v):.3f} | {max(v):.3f} |")
    Path(__file__).with_name("E13_F6_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
