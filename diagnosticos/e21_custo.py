"""E21 (plano: diagnosticos/E21_PLANO.md): decomposição do custo da v0.53 (M1 r5 + M2 Q2). Só descrição.
Uso: python -m diagnosticos.e21_custo FAM ...  |  --resumo"""
import json
import sys
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from analises import m2_e16 as E
from diagnosticos.e13_comum import refnome

SAIDA = Path(__file__).with_name("e21")


def familia(fam):
    origem, s = next(iter(E._series(fam)))
    y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
    T, d = X.shape
    m = M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), referencia=refnome(s), porta=True, eps_porta=0.002,
                   recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod_q2", precisao="r5")
    p = m.precisao
    rls = {"fp": 0.0}
    orig = p._rls

    def _rls(z, yy):
        a = p.fp
        orig(z, yy)
        rls["fp"] += p.fp - a
    p._rls = _rls
    M.rodar(m, X, y)
    n = m.base.n_steps
    core = m.base._core.fp
    r = dict(familia=fam, serie=s["nome"], d=d, T=T, v052={k: v / n for k, v in core.items()},
             v052_total=m.base.cost_per_step, m2=m.fp_porta / n, m1_rls=rls["fp"] / n, m1_resto=(p.fp - rls["fp"]) / n,
             k=len(p.w) if p.w is not None else None, total=m.cost_per_step)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{fam}.json").write_text(json.dumps(r, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(fam, {k: (round(v, 1) if isinstance(v, float) else v) for k, v in r.items() if k != "v052"}, flush=True)


def resumo():
    L = ["# Diagnóstico E21: decomposição do custo da v0.53 (FP por passo, uma série por família)", "",
         "| Família | d | k | v0.52 | (memória / estrutura / experimentos / triagem / controle) | M2 | M1 RLS | M1 resto | total | ÷ v0.52 |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    tot = []
    for f in E.TODAS:
        p = SAIDA / f"{f}.json"
        if not p.exists():
            continue
        r = json.loads(p.read_text(encoding="utf-8"))
        v = r["v052"]
        L.append(f"| {f} | {r['d']} | {r['k']} | {r['v052_total']:.0f} | {v['memory']:.0f} / {v['structure']:.0f} / "
                 f"{v['experiments']:.0f} / {v['screening']:.0f} / {v['control']:.0f} | {r['m2']:.0f} | {r['m1_rls']:.0f} | "
                 f"{r['m1_resto']:.0f} | {r['total']:.0f} | {r['total'] / r['v052_total']:.2f} |")
        tot.append(r)
    med = lambda k: float(np.median([r[k] for r in tot]))
    L += ["", f"Medianas: v0.52 {med('v052_total'):.0f}, M2 {med('m2'):.0f}, M1 RLS {med('m1_rls'):.0f}, "
          f"M1 resto {med('m1_resto'):.0f}, total {med('total'):.0f}."]
    Path(__file__).with_name("E21_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[-1:]))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo()
    else:
        for f_ in sys.argv[1:]:
            familia(f_)
