"""Medição M5B_E1 (plano: analises/M5B_E1_PLANO.md): M5b rascunho 0 (protótipo no commit cfb0321), Lebre054 com m5b=False
contra m5b=True. Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit cfb0321 e LEBRE053_PROTO como antes):
  python -m analises.m5b_e1 FAM ...   |   python -m analises.m5b_e1 resumo
"""
import hashlib
import json
import math
import subprocess
import sys

import numpy as np

from analises import m2_e20 as E20
from analises import m5a_e1 as E
from lab.run import ROOT

Lebre054 = E.Lebre054
OUT = E.AQUI / "m5b_e1"
COMMIT = "cfb0321"
FAIXA = (0.90, 0.98)


def proto_info():
    sujo = subprocess.run(["git", "-C", str(E.P54), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if sujo.strip():
        raise SystemExit(f"protótipo da v0.54 com alterações não commitadas:\n{sujo}")
    commit = subprocess.run(["git", "-C", str(E.P54), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    if commit != COMMIT:
        raise SystemExit(f"M5B_E1 exige o protótipo no commit {COMMIT} (encontrado {commit})")
    return dict(commit=commit, screening_sha256=hashlib.sha256((E.P54 / "lebre054" / "screening.py").read_bytes()).hexdigest())


def equivalentes(a, b):
    """compara o relatório de equivalentes das entradas aceitas no fim da série (núcleo de a = original)."""
    ca, cb = a.core._core, b.core._core
    sd = np.sqrt(np.maximum(np.diag(ca.g_c), 1e-12))
    fora = dentro = disc_fora = disc_dentro = 0
    for u in ca.active:
        if u[0] != "in":
            continue
        i = u[1]; r = np.abs(ca.g_c[i]) / (sd[i] * sd)
        ea, eb = ca.equivalents(u), cb.equivalents(u)
        for j in range(ca.d):
            if j == i:
                continue
            na = FAIXA[0] <= r[j] <= FAIXA[1]
            d = (j in ea) != (j in eb)
            if na:
                dentro += 1; disc_dentro += d
            else:
                fora += 1; disc_fora += d
    return dict(pares_fora=fora, disc_fora=disc_fora, pares_dentro=dentro, disc_dentro=disc_dentro)


def familia(fam):
    info = proto_info(); series = []
    for origem, s in E20._series(fam):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape
        kw = dict(season=s.get("season"), season2=s.get("season2"), reference=E.refnome(s))
        a, b = Lebre054(d, **kw), Lebre054(d, m5b=True, **kw)
        fa, fb = np.full(T, np.nan), np.full(T, np.nan)
        for t in range(T):
            yt = None if not math.isfinite(y[t]) else float(y[t])
            fa[t] = a.step(X[t], yt).value; fb[t] = b.step(X[t], yt).value
        series.append(dict(serie=s.get("nome"), origem=origem, T=T, d=d,
                           identica=bool(np.array_equal(fa, fb, equal_nan=True)), estrutura_igual=a.structure == b.structure,
                           nucleo_sem=a.core.cost_per_step, nucleo_com=b.core.cost_per_step,
                           total_sem=a.cost_per_step, total_com=b.cost_per_step, equiv=equivalentes(a, b)))
        print(fam, s.get("nome"), {k: v for k, v in series[-1].items() if k not in ("serie", "origem")}, flush=True)
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fam}.json").write_text(json.dumps(dict(familia=fam, prototipo=info, series=series), indent=1,
                                                ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def resumo():
    R = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8")) for f in E20.TODAS}
    S = [s for r in R.values() for s in r["series"]]
    c1 = all(s["identica"] and s["estrutura_igual"] for s in S)
    menor = all(s["nucleo_com"] < s["nucleo_sem"] for s in S)
    a50 = [s for s in R["A01"]["series"] if s["d"] == 50]
    r50 = float(np.mean([s["nucleo_com"] for s in a50]) / np.mean([s["nucleo_sem"] for s in a50]))
    a12 = R["A12"]["series"]
    r12 = float(np.mean([s["nucleo_com"] for s in a12]) / np.mean([s["nucleo_sem"] for s in a12]))
    c2 = menor and r50 <= 0.80 and r12 <= 0.80
    eq = {k: sum(s["equiv"][k] for s in S) for k in ("pares_fora", "disc_fora", "pares_dentro", "disc_dentro")}
    c3 = eq["disc_fora"] == 0
    L = ["# Medição M5B_E1 (M5b rascunho 0): resultado", "",
         f"Plano `M5B_E1_PLANO.md`. Protótipo no commit `{COMMIT}`; `Lebre054` com `m5b=False` contra `m5b=True`; "
         f"{len(R)} famílias do E20, {len(S)} séries.", "",
         "| Família | séries | idênticas | núcleo sem → com (média) | razão | total sem → com | equivalentes: discordâncias fora / dentro da faixa |",
         "|---|---|---|---|---|---|---|"]
    for f, r in R.items():
        ss = r["series"]; ns, nc = np.mean([s["nucleo_sem"] for s in ss]), np.mean([s["nucleo_com"] for s in ss])
        L.append(f"| {f} | {len(ss)} | {sum(s['identica'] and s['estrutura_igual'] for s in ss)} | {ns:.0f} → {nc:.0f} | "
                 f"{nc / ns:.3f} | {np.mean([s['total_sem'] for s in ss]):.0f} → {np.mean([s['total_com'] for s in ss]):.0f} | "
                 f"{sum(s['equiv']['disc_fora'] for s in ss)} / {sum(s['equiv']['disc_dentro'] for s in ss)} |")
    L += ["", f"1. **Identidade** (previsões e estrutura final, todas as séries): {'atende' if c1 else 'não atende'}",
          f"2. **Custo** (núcleo menor em todas as séries: {'sim' if menor else 'não'}; razão A01 d = 50: {r50:.3f}; "
          f"A12: {r12:.3f}; limite 0,80): {'atende' if c2 else 'não atende'}",
          f"3. **Equivalentes** (fora da faixa {FAIXA[0]}–{FAIXA[1]}: {eq['disc_fora']} discordâncias em {eq['pares_fora']} "
          f"pares; dentro: {eq['disc_dentro']} em {eq['pares_dentro']}, só reportado): {'atende' if c3 else 'não atende'}", "",
          f"**Decisão pela regra do plano:** a M5b (rascunho 0) é **{'aceita' if c1 and c2 and c3 else 'não aceita'}**."]
    (E.AQUI / "M5B_E1_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
