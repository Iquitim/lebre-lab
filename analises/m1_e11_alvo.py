"""Critérios próprios da M1, rascunho 1 (plano: analises/M1_E11_PLANO.md; ALGORITHM_SPEC_DRAFT_M1_r1.md, seções 1 e 3):
1. F6 em B03: custo da v0.53 <= 2,5 vezes o da v0.52 e erro (geo ÷ comparador completo) <= 1,05 × o menor erro entre as
   variantes do E10 com custo <= o da v0.53.
2. B01 e B02: limite superior do IC 95% de (M1 + M2) ÷ (M2 sozinha) <= 1,02 (bootstrap de blocos pareado, B = 2000).
Derivado de m1_e8_alvo.py (inalterado).

Uso: python -m analises.m1_e11_alvo
"""
import json
import math

import numpy as np

from analises import m2_dev as M
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

SEMENTE = 20261033
E10 = [(1.711, 872), (2.198, 198), (1.359, 2082), (1.574, 318), (1.101, 11432), (1.302, 1574), (1.000, 34200), (1.239, 4406)]  # (erro, FP) do E10
KW = dict(porta=True, eps_porta=0.002, recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod")


def main():
    info = M.proto_info()
    out = dict(prototipo=info, semente=SEMENTE, familias={})
    for fam in ("B03", "B01", "B02"):
        mod = load(ROOT / "scenarios" / M.ARQ[fam])
        series, reps = [], []
        for k, i in enumerate(mod.SPEC["sementes"]):
            s = mod.gerar(i)
            y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape
            season, season2 = s.get("season"), s.get("season2")
            ref = "sazonal" if season else "persistencia"
            ini = int(0.2 * T)
            m1 = M.Lebre053(d, season=season, season2=season2, referencia=ref, precisao="r1", **KW)
            m2 = M.Lebre053(d, season=season, season2=season2, referencia=ref, precisao=False, **KW)
            f1, f2 = M.rodar(m1, X, y), M.rodar(m2, X, y)
            fl = M.rodar_ref(OnlineLinear(d), X, y)
            m52 = M.Lebre053(d, season=season, season2=season2, porta=False)
            f52 = M.rodar(m52, X, y)
            mse = {n: forecast_metrics(y, f, ini)["mse"] for n, f in (("m1m2", f1), ("m2", f2), ("linear", fl), ("v052", f52))}
            p, rep = M.par_bootstrap(y, f1, f2, ini, M.bloco(fam), np.random.default_rng([SEMENTE, k, len(fam)]))
            reps.append(rep)
            p1 = m1.precisao
            series.append(dict(serie=s["nome"], d=d, mse=mse, m1m2_sobre_linear=mse["m1m2"] / mse["linear"],
                               m1m2_sobre_m2=p, v052_sobre_linear=mse["v052"] / mse["linear"],
                               selecionadas=[s["entradas"][j] for j in p1.sel] if p1.sel is not None else None,
                               peso_especialista_final=p1.prod.s(), custo_m1m2=m1.cost_per_step, custo_m2=m2.cost_per_step,
                               custo_v052=m52.cost_per_step))
            print(fam, s["nome"], {k_: round(v, 4) for k_, v in series[-1].items() if isinstance(v, float)}, flush=True)
        rr = np.vstack(reps).mean(0); rr = rr[np.isfinite(rr)]
        out["familias"][fam] = dict(
            series=series,
            geo_m1m2_sobre_linear=float(np.exp(np.mean([math.log(x["m1m2_sobre_linear"]) for x in series]))),
            geo_v052_sobre_linear=float(np.exp(np.mean([math.log(x["v052_sobre_linear"]) for x in series]))),
            geo_m1m2_sobre_m2=float(np.exp(np.mean([math.log(x["m1m2_sobre_m2"]) for x in series]))),
            ic95_m1m2_sobre_m2=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))])
    F = out["familias"]
    sb = F["B03"]["series"]
    custo = float(np.mean([x["custo_m1m2"] for x in sb])); custo52 = float(np.mean([x["custo_v052"] for x in sb]))
    melhor = min(e for e, c in E10 if c <= custo)
    c1 = custo <= 2.5 * custo52 and F["B03"]["geo_m1m2_sobre_linear"] <= 1.05 * melhor
    out["f6"] = dict(custo_v053=custo, custo_v052=custo52, razao_custo=custo / custo52, melhor_variante_no_custo=melhor,
                     meta=1.05 * melhor, obtido=F["B03"]["geo_m1m2_sobre_linear"])
    c2 = all(F[f]["ic95_m1m2_sobre_m2"][1] <= 1.02 for f in ("B01", "B02"))
    out["criterios"] = {"1_F6_fronteira": c1, "2_B01_B02_vs_M2": c2}
    (M.AQUI / "m1e11_alvo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    L = ["# Experimento E11: critérios próprios da M1 (rascunho 1)", "",
         f"Protótipo `{info['commit']}`. Plano `M1_E11_PLANO.md`.", "",
         f"F6: custo da v0.53 em B03 {custo:.0f} FP ({custo / custo52:.2f} × v0.52, teto 2,5); melhor variante com custo <= "
         f"esse: erro {melhor:.3f}; meta {1.05 * melhor:.3f}; obtido {F['B03']['geo_m1m2_sobre_linear']:.3f}.", "",
         "| Família | (M1+M2) ÷ linear (geo) | v0.52 ÷ linear (geo) | (M1+M2) ÷ M2 (IC 95%) |", "|---|---|---|---|"]
    for f, v in F.items():
        L.append(f"| {f} | {v['geo_m1m2_sobre_linear']:.3f} | {v['geo_v052_sobre_linear']:.3f} | {v['geo_m1m2_sobre_m2']:.3f} "
                 f"({v['ic95_m1m2_sobre_m2'][0]:.3f}–{v['ic95_m1m2_sobre_m2'][1]:.3f}) |")
    L += ["", f"Critério 1 (F6, fronteira): {'sim' if c1 else '**não**'}. Critério 2 (B01, B02 <= 1,02 da M2): "
          f"{'sim' if c2 else '**não**'}.", ""]
    (M.AQUI / "M1_E11_ALVO_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
