"""Diagnóstico E23 (plano: diagnosticos/E23_PLANO.md): linha de base da v0.53 (lebre==0.2.0) para as prioridades da
v0.54. Só descritivo. Rodar da raiz do Lab, num ambiente com lebre==0.2.0:  python -m diagnosticos.e23_base_v054
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

import lebre
from lab.baselines import Naive, OnlineLinear
from lab.metrics import forecast_metrics, structure_metrics
from lab.run import load

if lebre.__version__ != "0.2.0":
    raise SystemExit(f"E23 exige lebre==0.2.0 (encontrada {lebre.__version__})")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagnosticos" / "e23_base_v054.json"
SC = {k: load(ROOT / "scenarios" / p) for k, p in [("A01", "A/A01_muitas_entradas.py"), ("A02", "A/A02_nulo.py"),
                                                    ("A05", "A/A05_mudanca_regime.py"), ("A12", "A/A12_escala.py"),
                                                    ("C03", "C/C03_niveis_de_preco.py"), ("D02", "D/D02_ciclos_declarados.py")]}
INTERNAL = ("own_past", "residual_state")


def geo(v):
    v = np.asarray([x for x in v if x is not None], float); v = v[np.isfinite(v) & (v > 0)]
    return float(np.exp(np.mean(np.log(v)))) if len(v) else float("nan")


def run_model(m, y, X, start):
    T = len(y); f = np.full(T, np.nan)
    for t in range(T):
        f[t] = m.step(X[t], None if not math.isfinite(y[t]) else float(y[t])).value
    return forecast_metrics(y, f, start)["mse"]


def comparators(y, X, start):
    out = {}
    for mm in (Naive(X.shape[1]), OnlineLinear(X.shape[1])):
        f = np.full(len(y), np.nan)
        for t in range(len(y)):
            f[t] = mm.predict(X[t]); mm.observe(None if not math.isfinite(y[t]) else float(y[t]))
        out[mm.name] = forecast_metrics(y, f, start)["mse"]
    return out


def series_both(s, warmup, comps=True, season_override=None):
    y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
    start = int(warmup * len(y))
    season, season2 = (s.get("season"), s.get("season2")) if season_override is None else season_override
    full = lebre.Lebre(X.shape[1], season=season, season2=season2)
    core = lebre.Lebre(X.shape[1], season=season, season2=season2, core_only=True)
    r = dict(nome=s.get("nome"), grupo=s.get("grupo"), d=X.shape[1], T=len(y),
             mse_v053=run_model(full, y, X, start), mse_core=run_model(core, y, X, start),
             custo_v053=full.cost_per_step, custo_core=core.cost_per_step,
             custo_m1=full._m1.fp / full.n_steps, custo_m2=full._fp_extra / full.n_steps,
             peso_m1=full.layer_weights["m1"], estrutura_igual=full.structure == core.structure and
             [(e.t, e.outcome, e.change, e.added, e.removed) for e in full.events if e.change != "gate"] ==
             [(e.t, e.outcome, e.change, e.added, e.removed) for e in core.events],
             estrutura_final=full.structure,
             eventos=[dict(t=e.t, resultado=e.outcome, mudanca=e.change, entra=e.added, sai=e.removed) for e in full.events])
    if comps:
        r["comparadores"] = comparators(y, X, start)
    if s.get("truth") is not None:
        st = structure_metrics([e for e in full.events if e.change != "gate"], full.structure, s["truth"])
        r.update(recall=st["recall"], falsas_aceitas=st["falsas_aceitas"], finais_falsas=st["finais_falsas"])
    return r


def main():
    R = {"versao_lebre": lebre.__version__}
    w = lambda k: SC[k].SPEC["aquecimento"]
    print("A01 ...", flush=True)
    R["A01"] = [series_both(SC["A01"].gerar(sd), w("A01"), comps=False) for sd in SC["A01"].SPEC["sementes"]]
    print("A02 ...", flush=True)
    R["A02"] = [series_both(SC["A02"].gerar(sd), w("A02"), comps=False) for sd in SC["A02"].SPEC["sementes"]]
    print("A05 ...", flush=True)
    R["A05"] = [series_both(SC["A05"].gerar(sd), w("A05")) for sd in SC["A05"].SPEC["sementes"]]
    print("C03 ...", flush=True)
    R["C03"] = [series_both(SC["C03"].gerar(sd), w("C03")) for sd in SC["C03"].SPEC["sementes"]]
    print("D02 ...", flush=True)
    R["D02"] = []
    for i in SC["D02"].SPEC["sementes"]:
        s = SC["D02"].gerar(i)
        a = series_both(s, w("D02"), comps=False)
        b = series_both(s, w("D02"), comps=False, season_override=(None, None))
        R["D02"].append(dict(nome=s.get("nome"), grupo=s["grupo"], ciclo_certo=a, sem_ciclo=b,
                             v053_sem_sobre_certo=b["mse_v053"] / a["mse_v053"], core_sem_sobre_certo=b["mse_core"] / a["mse_core"]))
    print("A12 ...", flush=True)
    R["A12"] = [series_both(SC["A12"].gerar(sd), w("A12"), comps=False) for sd in SC["A12"].SPEC["sementes"]]
    fin = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "Codinome Lebre" / "experiments" / "LEBRE-V0.53-FINAL-01" / "final_resultado.json"
    if fin.exists():
        S = json.loads(fin.read_text(encoding="utf-8"))["series"]
        z = [x for x in S if (x["peso_m1_final"] or 0) < 1e-3]
        R["final_peso_m1_zero"] = dict(n=len(z), n_total=len(S), familias=sorted({x["familia"] for x in z}),
                                       acrescimo_mediano=float(np.median([x["acrescimo_custo"] for x in z])),
                                       razao_custo_mediana=float(np.median([x["custo_v053"] / x["custo_v052"] for x in z])))
    OUT.write_text(json.dumps(R, indent=1, ensure_ascii=False), encoding="utf-8")
    resumo(R)


def resumo(R):
    def lin(*c):
        print("| " + " | ".join(str(x) for x in c) + " |")
    print("\n## 1. Custo")
    for d in (10, 20, 50):
        g = [r for r in R["A01"] if r["d"] == d]
        lin(f"A01 d={d}", f"{np.mean([r['custo_core'] for r in g]):.0f}", f"{np.mean([r['custo_v053'] for r in g]):.0f}",
            f"M1 {np.mean([r['custo_m1'] for r in g]):.0f}", f"M2 {np.mean([r['custo_m2'] for r in g]):.0f}",
            f"recall {np.mean([r['recall'] for r in g]):.2f}", f"falsas {sum(r['falsas_aceitas'] > 0 for r in g)}/{len(g)}",
            f"peso M1 med {np.median([r['peso_m1'] for r in g]):.2f}", f"v053/core {geo([r['mse_v053'] / r['mse_core'] for r in g]):.3f}")
    for r in R["A12"]:
        lin("A12 d=50 T=200k", f"{r['custo_core']:.0f}", f"{r['custo_v053']:.0f}", f"M1 {r['custo_m1']:.0f}", f"M2 {r['custo_m2']:.0f}",
            f"peso M1 {r['peso_m1']:.2f}", f"v053/core {r['mse_v053'] / r['mse_core']:.3f}")
    if "final_peso_m1_zero" in R:
        print("final, peso M1 zero:", R["final_peso_m1_zero"])
    print("\n## 2. Remoções (A05)")
    a = R["A05"]
    rem = sum(any(e["resultado"] == "accepted" and e["sai"] and e["sai"].startswith("x0") for e in r["eventos"]) for r in a)
    fica = sum("x0" in [u.split("[")[0] for u in r["estrutura_final"]] for r in a)
    lin("A05", f"x0 removida {rem}/20", f"x0 no fim {fica}/20",
        f"v053/linear {geo([r['mse_v053'] / r['comparadores']['linear_online'] for r in a]):.3f}",
        f"core/linear {geo([r['mse_core'] / r['comparadores']['linear_online'] for r in a]):.3f}",
        f"peso M1 med {np.median([r['peso_m1'] for r in a]):.2f}", f"estrutura igual {sum(r['estrutura_igual'] for r in a)}/20")
    print("\n## 3. Níveis (C03)")
    c = R["C03"]
    ext = lambda r: [u for u in r["estrutura_final"] if u.split("[")[0] not in INTERNAL]
    acc = lambda r: any(e["resultado"] == "accepted" and e["entra"] and e["entra"].split("[")[0] not in INTERNAL and e["mudanca"] != "gate" for e in r["eventos"])
    for r in c:
        nv = r["comparadores"]["ingenuo"]
        lin(r["nome"], f"aceita externa {acc(r)}", f"fim {ext(r)}", f"v053/ingênuo {r['mse_v053'] / nv:.3f}", f"core/ingênuo {r['mse_core'] / nv:.3f}")
    print("\n## 4. Nulo (A02)")
    lin("A02", f"séries com falsa {sum(r['falsas_aceitas'] > 0 for r in R['A02'])}/40", f"estrutura igual {sum(r['estrutura_igual'] for r in R['A02'])}/40")
    print("\n## 5. Ciclo (D02)")
    for g in ("B02", "B01"):
        rr = [r for r in R["D02"] if r["grupo"] == g]
        lin(g, len(rr), f"v053 sem/certo {geo([r['v053_sem_sobre_certo'] for r in rr]):.3f}", f"core sem/certo {geo([r['core_sem_sobre_certo'] for r in rr]):.3f}")
    rr = R["D02"]
    lin("todas", len(rr), f"v053 sem/certo {geo([r['v053_sem_sobre_certo'] for r in rr]):.3f}", f"core sem/certo {geo([r['core_sem_sobre_certo'] for r in rr]):.3f}")


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo(json.loads(OUT.read_text(encoding="utf-8")))
    else:
        main()
