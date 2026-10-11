"""Medição M4_E1 (plano: analises/M4_E1_PLANO.md): M4 rascunho 0 (protótipo no commit 438ac08), Lebre054 com m4=False
contra m4=True (os dois com a M5a, sem a M5b). Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit 438ac08 e
LEBRE053_PROTO como antes):
  python -m analises.m4_e1 FAM ...   |   python -m analises.m4_e1 resumo
"""
import hashlib
import json
import math
import subprocess
import sys

import numpy as np

from analises import m2_dev as M
from analises import m2_e20 as E20
from analises import m5a_e1 as E

Lebre054 = E.Lebre054
OUT = E.AQUI / "m4_e1"
COMMIT = "438ac08"
SEMENTE_BOOT = 20261340
TROCA = 15000


def proto_info():
    sujo = subprocess.run(["git", "-C", str(E.P54), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if sujo.strip():
        raise SystemExit(f"protótipo da v0.54 com alterações não commitadas:\n{sujo}")
    commit = subprocess.run(["git", "-C", str(E.P54), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    if commit != COMMIT:
        raise SystemExit(f"M4_E1 exige o protótipo no commit {COMMIT} (encontrado {commit})")
    return dict(commit=commit, removal_sha256=hashlib.sha256((E.P54 / "lebre054" / "removal.py").read_bytes()).hexdigest())


def eventos(m):
    c = m.core._core
    return [dict(t=e[0], tipo=e[2], entra=list(e[3]) if e[3] else None, sai=list(e[4]) if e[4] else None)
            for e in c.events if e[1] == "accepted"]


def externas_aceitas(ev, d):
    return sorted({e["entra"][1] for e in ev if e["entra"] and e["entra"][0] == "in" and e["entra"][1] < d})


def familia(fam):
    info = proto_info(); curtas = fam in E20.CURTAS
    series, reps = [], []
    for k, (origem, s) in enumerate(E20._series(fam)):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape
        kw = dict(season=s.get("season"), season2=s.get("season2"), reference=E.refnome(s))
        a, b = Lebre054(d, **kw), Lebre054(d, m4=True, **kw)
        fa, fb = np.full(T, np.nan), np.full(T, np.nan)
        for t in range(T):
            yt = None if not math.isfinite(y[t]) else float(y[t])
            fa[t] = a.step(X[t], yt).value; fb[t] = b.step(X[t], yt).value
        ini = int(0.2 * T)
        L = E20.bloco_curta(origem) if curtas else E20.bloco(fam)
        p, rep = M.par_bootstrap(y, fb, fa, ini, L, np.random.default_rng([SEMENTE_BOOT, E20.TODAS.index(fam), k]))
        reps.append(rep)
        ea, eb = eventos(a), eventos(b)
        series.append(dict(serie=s.get("nome"), origem=origem, T=T, d=d, razao=p,
                           nan_aval=int((np.isfinite(y) & ~np.isfinite(fb))[ini:].sum()),
                           identica=bool(np.array_equal(fa, fb, equal_nan=True)), sem_aceite=len(ea) == 0,
                           remocoes=[e for e in eb if e["tipo"] == "rem"],
                           estrutura_sem=a.structure, estrutura_com=b.structure,
                           externas_aceitas_sem=externas_aceitas(ea, d), externas_aceitas_com=externas_aceitas(eb, d),
                           custo_sem=a.cost_per_step, custo_com=b.cost_per_step))
        print(fam, s.get("nome"), "razão", round(p, 5), "remoções", series[-1]["remocoes"], flush=True)
    logs = np.array([math.log(r["razao"]) for r in series if np.isfinite(r["razao"]) and r["razao"] > 0])
    rr = np.vstack(reps).mean(0); rr = rr[np.isfinite(rr)]
    resumo = dict(geo=float(np.exp(logs.mean())), ic95=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))],
                  n=len(series), nan_aval=int(sum(r["nan_aval"] for r in series)),
                  remocoes=int(sum(len(r["remocoes"]) for r in series)),
                  identidade_ok=all(r["identica"] for r in series if r["sem_aceite"]),
                  custo_sem=float(np.mean([r["custo_sem"] for r in series])), custo_com=float(np.mean([r["custo_com"] for r in series])))
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fam}.json").write_text(json.dumps(dict(familia=fam, prototipo=info, semente=SEMENTE_BOOT, resumo=resumo,
                                                     series=series), indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
    print(fam, "resumo", resumo, flush=True)


def resumo():
    R = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8")) for f in E20.TODAS}
    a05 = R["A05"]["series"]
    rem_a05 = sum(any(e["sai"] == ["in", 0] and TROCA <= e["t"] <= TROCA + 10000 for e in s["remocoes"]) for s in a05)
    c1 = rem_a05 >= 14
    falsas_a01 = sum(any(e["sai"] in (["in", 0], ["in", 1]) for e in s["remocoes"]) for s in R["A01"]["series"])
    falsas_a02 = sum(any(n.startswith("x") for n in s["estrutura_com"]) for s in R["A02"]["series"])
    c2 = falsas_a01 == 0 and falsas_a02 == 0
    c3 = all(r["resumo"]["ic95"][1] <= 1.02 and r["resumo"]["nan_aval"] == 0 for r in R.values())
    c4 = all(r["resumo"]["identidade_ok"] for r in R.values())
    pior = max(R.items(), key=lambda kv: kv[1]["resumo"]["ic95"][1])
    c03 = R["C03"]["series"]
    L = ["# Medição M4_E1 (M4 rascunho 0): resultado", "",
         f"Plano `M4_E1_PLANO.md`. Protótipo no commit `{COMMIT}`; `Lebre054` com `m4=False` contra `m4=True` (os dois com a "
         f"M5a, sem a M5b); {len(R)} famílias do E20.", "",
         "| Família | séries | com M4 ÷ sem M4 (MSE) | IC 95% | remoções | custo sem → com |", "|---|---|---|---|---|---|"]
    for f, r in R.items():
        z = r["resumo"]
        L.append(f"| {f} | {z['n']} | {z['geo']:.4f} | {z['ic95'][0]:.4f}–{z['ic95'][1]:.4f} | {z['remocoes']} | "
                 f"{z['custo_sem']:.0f} → {z['custo_com']:.0f} |")
    L += ["", f"1. **A05** (x0 removida até 10.000 passos depois da troca, ≥ 14 de 20): {rem_a05} de 20 — "
              f"{'atende' if c1 else 'não atende'}",
          f"2. **Sem remoções falsas** (A01: séries com entrada verdadeira removida = {falsas_a01}; A02: séries com entrada "
          f"falsa na estrutura final = {falsas_a02}): {'atende' if c2 else 'não atende'}",
          f"3. **Sem piora** (limite superior ≤ 1,02 em todas; pior: {pior[0]}, {pior[1]['resumo']['ic95'][1]:.4f}; nenhuma "
          f"previsão não finita): {'atende' if c3 else 'não atende'}",
          f"4. **Identidade** onde nenhuma unidade foi aceita: {'atende' if c4 else 'não atende'}", "",
          "Reportado (C03, entradas externas): estrutura final sem M4 "
          f"{sum(any(n.startswith('x') for n in s['estrutura_sem']) for s in c03)} de {len(c03)}, com M4 "
          f"{sum(any(n.startswith('x') for n in s['estrutura_com']) for s in c03)} de {len(c03)}; aceitas em algum momento "
          f"{sum(bool(s['externas_aceitas_com']) for s in c03)} de {len(c03)}.", "",
          f"**Decisão pela regra do plano:** a M4 (rascunho 0) **{'segue para validação em dados novos' if c1 and c2 and c3 and c4 else 'não segue'}**."]
    (E.AQUI / "M4_E1_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("feito")


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
