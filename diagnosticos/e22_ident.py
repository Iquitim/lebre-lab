"""E22 (plano: diagnosticos/E22_PLANO.md): MSE da v0.53 com o código novo == MSE registrado com bca5dac, série a série.
Uso: python -m diagnosticos.e22_ident ORIGEM FAM ...  (ORIGEM = e20 | val5)  |  --resumo"""
import json
import sys
from pathlib import Path

import numpy as np

from analises import m1_val5 as V5
from analises import m2_dev as M
from analises import m2_e20 as E
from analises.m2_dev_r6 import rodar
from lab.metrics import forecast_metrics

AQUI = M.AQUI
SAIDA = Path(__file__).with_name("e22")


def familia(origem, fam):
    mod = E if origem == "e20" else V5
    reg = json.loads(((AQUI / "e20_prod_q2") if origem == "e20" else (AQUI / "m1val5")).joinpath(f"{fam}.json")
                     .read_text(encoding="utf-8"))["series"]
    out = []
    for k, (o, s) in enumerate(mod._series(fam)):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape
        ini = int(0.2 * T)
        zero, season = s.get("zero_baseline"), s.get("season")
        refnome = "zero" if zero else ("sazonal" if season else "persistencia")
        m = M.Lebre053(d, season=season, season2=s.get("season2"), referencia=refnome, porta=True, eps_porta=0.002,
                       recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod_q2", precisao="r5")
        f, _ = rodar(m, X, y)
        mse = forecast_metrics(y, f, ini)["mse"]
        r = reg[k]
        assert r["serie"] == s["nome"]
        out.append(dict(serie=s["nome"], igual=mse == r["mse"], mse=mse, mse_registrado=r["mse"],
                        custo_novo=m.cost_per_step, custo_antigo=r["acrescimo_custo"] + r["custo_v052"]))
        if mse != r["mse"]:
            print(origem, fam, s["nome"], "DIFERE", mse, r["mse"], flush=True)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{origem}_{fam}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                                newline="\n")
    print(origem, fam, "iguais:", sum(x["igual"] for x in out), "de", len(out), flush=True)


def resumo():
    R = [x for p in sorted(SAIDA.glob("*.json")) for x in json.loads(p.read_text(encoding="utf-8"))]
    dif = [x for x in R if not x["igual"]]
    rel = [x["custo_novo"] / x["custo_antigo"] for x in R]
    L = ["# Verificação E22 (M5): resultado", "", "Plano `E22_PLANO.md`.", "",
         f"Séries conferidas: {len(R)}; com MSE diferente do registrado: {len(dif)}.", "",
         f"Custo contado novo ÷ antigo: mediana {np.median(rel):.3f} (mín {min(rel):.3f}, máx {max(rel):.3f})."]
    L += [f"- {x['serie']}: {x['mse']!r} contra {x['mse_registrado']!r}" for x in dif]
    Path(__file__).with_name("E22_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo()
    else:
        for f_ in sys.argv[2:]:
            familia(sys.argv[1], f_)
