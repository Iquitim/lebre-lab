"""Auditoria E18 (plano: diagnosticos/E18_PLANO.md): passos de avaliação com alvo finito e previsão não finita.
Uso: python -m diagnosticos.e18_nan CONFIG FAM ...   |   --resumo"""
import json
import sys
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from analises import m2_e16 as E
from diagnosticos.e13_comum import refnome

CONFIGS = {"prod": dict(saida="prod"), "prod_q": dict(saida="prod_q"), "prod_r2": dict(saida="prod", precisao="r2")}
SAIDA = Path(__file__).with_name("e18")


def familia(config, fam):
    res = []
    for origem, s in E._series(fam):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape
        ini = int(0.2 * T)
        m = M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), referencia=refnome(s), porta=True,
                       eps_porta=0.002, recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True,
                       **CONFIGS[config])
        f = M.rodar(m, X, y)
        ruim = np.isfinite(y) & ~np.isfinite(f)
        ruim[:ini] = False
        n = int(ruim.sum())
        res.append(dict(serie=s["nome"], origem=origem, n_nan=n, primeiro=int(np.argmax(ruim)) if n else None,
                        n_aval=int((np.isfinite(y[ini:])).sum())))
        if n:
            print(config, fam, s["nome"], "NaN:", n, "de", res[-1]["n_aval"], "desde", res[-1]["primeiro"], flush=True)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{config}_{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                                newline="\n")
    print(config, fam, "feito", flush=True)


def resumo():
    L = ["# Auditoria E18: previsões NaN não contadas (resultado)", "", "Plano `E18_PLANO.md`.", "",
         "| Config | Família | Série | passos NaN / avaliação | primeiro |", "|---|---|---|---|---|"]
    tot = {}
    for p in sorted(SAIDA.glob("*.json")):
        config, fam = p.stem.split("_", 1) if not p.stem.startswith("prod_") else ("_".join(p.stem.split("_")[:2]),
                                                                                    "_".join(p.stem.split("_")[2:]))
        for r in json.loads(p.read_text(encoding="utf-8")):
            tot.setdefault(config, [0, 0])
            tot[config][1] += 1
            if r["n_nan"]:
                tot[config][0] += 1
                L.append(f"| {config} | {fam} | {r['serie']} | {r['n_nan']} / {r['n_aval']} | {r['primeiro']} |")
    L += ["", "Séries afetadas / auditadas: " + "; ".join(f"{c}: {a} / {b}" for c, (a, b) in tot.items())]
    Path(__file__).with_name("E18_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo()
    else:
        for f_ in sys.argv[2:]:
            familia(sys.argv[1], f_)
