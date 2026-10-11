"""Medição da validação 6 (regras e critérios: analises/VALIDACAO6_PLANO.md; congelamento: VALIDACAO6_CONGELADA.md).
M5a rascunho 2 (protótipo no commit f69dec4) contra a v0.53 (lebre==0.2.0). Usa as funções de analises/m5a_e1.py sem
alteração. Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit f69dec4 e LEBRE053_PROTO como antes):
  python -m analises.m5a_val6 FAM ...   |   python -m analises.m5a_val6 resumo
"""
import json
import math
import sys

import numpy as np

from analises import m5a_e1 as E
from lab.run import ROOT, load

OUT = E.AQUI / "m5a_val6"
SEMENTE_BOOT = 20261063
FAMILIAS = {"U-A01": "UA01_custo", "U-A05": "UA05_custo", "U-B02": "UB02_carga", "U-B03": "UB03_qualidade_do_ar",
            "U-B06": "UB06_eolica", "U-B07": "UB07_mare"}
CUSTO = ("U-A01", "U-A05")


def familia(fid):
    info = E.proto_info()
    if info["commit"] != "f69dec4":
        raise SystemExit(f"validação 6 exige o protótipo no commit f69dec4 (encontrado {info['commit']})")
    mod = load(ROOT / "scenarios" / "U" / f"{FAMILIAS[fid]}.py")
    L = 168 if fid.startswith("U-B") else 20
    series, reps = [], []
    for k, sd in enumerate(mod.SPEC["sementes"]):
        s = mod.gerar(sd)
        y, fa, fb, a, b, _, _ = E.par(s)
        ini = int(0.2 * len(y))
        p, rep = E.M.par_bootstrap(y, fb, fa, ini, L, np.random.default_rng([SEMENTE_BOOT, list(FAMILIAS).index(fid), k]))
        reps.append(rep)
        st = b.m1_state
        series.append(dict(serie=s.get("nome"), T=len(y), razao=p, sono=st,
                           nan_aval=int((np.isfinite(y) & ~np.isfinite(fb))[ini:].sum()),
                           identica=bool(np.array_equal(fa, fb, equal_nan=True)),
                           m1_v053=a._m1.fp / a.n_steps, m1_v054=st["m1_fp_per_step"],
                           total_v053=a.cost_per_step, total_v054=b.cost_per_step))
        print(fid, s.get("nome"), "razão", round(p, 5), "M1", round(series[-1]["m1_v053"]), "->",
              round(series[-1]["m1_v054"]), "sono", st, flush=True)
    logs = np.array([math.log(r["razao"]) for r in series])
    rr = np.vstack(reps).mean(0); rr = rr[np.isfinite(rr)]
    m53, m54 = float(np.mean([r["m1_v053"] for r in series])), float(np.mean([r["m1_v054"] for r in series]))
    resumo = dict(geo=float(np.exp(logs.mean())),
                  ic95=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))], n=len(series),
                  nan_aval=int(sum(r["nan_aval"] for r in series)), dormiram=int(sum(r["sono"]["sleeps"] > 0 for r in series)),
                  identidade_ok=all(r["identica"] for r in series if r["sono"]["sleeps"] == 0),
                  m1_v053=m53, m1_v054=m54, razao_custo_m1=m54 / m53,
                  total_v053=float(np.mean([r["total_v053"] for r in series])),
                  total_v054=float(np.mean([r["total_v054"] for r in series])))
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fid}.json").write_text(json.dumps(dict(familia=fid, prototipo=info, semente=SEMENTE_BOOT, bloco=L,
                                                     resumo=resumo, series=series), indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
    print(fid, "resumo", resumo, flush=True)


def resumo():
    R = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8"))["resumo"] for f in FAMILIAS}
    c1 = all(R[f]["razao_custo_m1"] <= 0.40 for f in CUSTO)
    c2 = all(r["ic95"][1] <= 1.01 and r["nan_aval"] == 0 for r in R.values())
    c3 = all(r["identidade_ok"] for r in R.values())
    L = ["# Validação 6 (v0.54, M5a rascunho 2): resultado", "",
         "Regras e critérios em `VALIDACAO6_PLANO.md`; congelamento em `VALIDACAO6_CONGELADA.md`. Protótipo no commit `f69dec4`; "
         "referência `lebre==0.2.0`. Usada uma única vez.", "",
         "| Família | séries | v0.54 ÷ v0.53 (MSE) | IC 95% | M1 dormiu | custo da M1 v0.53 → v0.54 | razão | custo total v0.53 → v0.54 |",
         "|---|---|---|---|---|---|---|---|"]
    for f, r in R.items():
        L.append(f"| {f} | {r['n']} | {r['geo']:.4f} | {r['ic95'][0]:.4f}–{r['ic95'][1]:.4f} | {r['dormiram']} | "
                 f"{r['m1_v053']:.0f} → {r['m1_v054']:.0f} | {r['razao_custo_m1']:.3f} | {r['total_v053']:.0f} → {r['total_v054']:.0f} |")
    L += ["", f"1. **Custo** (U-A01 e U-A05, razão ≤ 0,40): {'atende' if c1 else 'não atende'}",
          f"2. **Sem piora** (limite superior ≤ 1,01 em todas; nenhuma previsão não finita): {'atende' if c2 else 'não atende'}",
          f"3. **Identidade** onde a M1 nunca dormiu: {'atende' if c3 else 'não atende'}", "",
          f"**Decisão pela regra do plano:** a M5a (rascunho 2) é **{'aceita' if c1 and c2 and c3 else 'não aceita'}**."]
    (E.AQUI / "VALIDACAO6_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
