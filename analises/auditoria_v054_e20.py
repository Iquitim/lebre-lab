"""Auditoria da v0.54, teste T10 (plano: lebre-research experiments/LEBRE-V0.54-AUDIT-01/PLANO_AUDITORIA.md): a v0.54
inteira (Lebre054 com m5a, m5b e m4; protótipo no commit cfe72ce) contra a v0.53 (lebre==0.2.0) nas 64 famílias do E20.
Bootstrap de blocos pareado como no E20, semente 2026101301. Sinal de alerta: limite superior do IC 95% > 1,02.
Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit cfe72ce e LEBRE053_PROTO como antes):
  python -m analises.auditoria_v054_e20 FAM ...   |   python -m analises.auditoria_v054_e20 resumo
"""
import json
import math
import subprocess
import sys

import numpy as np

import lebre
from analises import m2_dev as M
from analises import m2_e20 as E20
from analises import m5a_e1 as E

OUT = E.AQUI / "auditoria_v054_e20"
COMMIT = "cfe72ce"
SEMENTE_BOOT = 2026101301
KW054 = dict(m5a=True, m5b=True, m4=True)


def proto_info():
    commit = subprocess.run(["git", "-C", str(E.P54), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(["git", "-C", str(E.P54), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if commit != COMMIT or sujo.strip():
        raise SystemExit(f"exige o protótipo limpo no commit {COMMIT} (encontrado {commit})")
    return dict(commit=commit)


def familia(fam):
    info = proto_info(); curtas = fam in E20.CURTAS
    series, reps = [], []
    for k, (origem, s) in enumerate(E20._series(fam)):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape; ini = int(0.2 * T)
        kw = dict(season=s.get("season"), season2=s.get("season2"), reference=E.refnome(s))
        a, b = lebre.Lebre(d, **kw), E.Lebre054(d, **kw, **KW054)
        fa, fb = np.full(T, np.nan), np.full(T, np.nan)
        for t in range(T):
            yt = None if not math.isfinite(y[t]) else float(y[t])
            fa[t] = a.step(X[t], yt).value; fb[t] = b.step(X[t], yt).value
        L = E20.bloco_curta(origem) if curtas else E20.bloco(fam)
        p, rep = M.par_bootstrap(y, fb, fa, ini, L, np.random.default_rng([SEMENTE_BOOT, E20.TODAS.index(fam), k]))
        reps.append(rep)
        series.append(dict(serie=s.get("nome"), T=T, razao=p, nan=int((np.isfinite(y) & ~np.isfinite(fb))[ini:].sum()),
                           custo53=a.cost_per_step, custo54=b.cost_per_step,
                           remocoes=sum(1 for e in b.core._core.events if e[1] == "accepted" and e[2] == "rem")))
        print(fam, s.get("nome"), round(p, 5), flush=True)
    logs = [math.log(x["razao"]) for x in series if np.isfinite(x["razao"]) and x["razao"] > 0]
    rr = np.vstack(reps).mean(0); rr = rr[np.isfinite(rr)]
    resumo = dict(geo=float(np.exp(np.mean(logs))), ic95=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))],
                  n=len(series), nan=int(sum(x["nan"] for x in series)), remocoes=int(sum(x["remocoes"] for x in series)),
                  custo=float(np.median([x["custo54"] / x["custo53"] for x in series])))
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fam}.json").write_text(json.dumps(dict(familia=fam, prototipo=info, resumo=resumo, series=series), indent=1,
                                                ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(fam, "resumo", resumo, flush=True)


def resumo():
    R = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8"))["resumo"] for f in E20.TODAS}
    alerta = [f for f, r in R.items() if r["ic95"][1] > 1.02 or r["nan"]]
    L = ["# Auditoria da v0.54, T10: a v0.54 inteira contra a v0.53 no banco do E20", "",
         "| Família | séries | v0.54 ÷ v0.53 | IC 95% | custo (mediana da razão) | remoções |", "|---|---|---|---|---|---|"]
    for f, r in R.items():
        L.append(f"| {f} | {r['n']} | {r['geo']:.4f} | {r['ic95'][0]:.4f}–{r['ic95'][1]:.4f} | {r['custo']:.3f} | {r['remocoes']} |")
    L += ["", f"**Sinais de alerta (limite superior > 1,02 ou previsão não finita):** {', '.join(alerta) or 'nenhum'}."]
    (E.AQUI / "AUDITORIA_V054_E20_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("feito")


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
