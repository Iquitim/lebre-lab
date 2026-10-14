"""Errata 01 da v0.54 (plano: analises/ERRATA01_V054_PLANO.md): M5b rascunho 2 (protótipo f9906c4) contra a v0.54
promovida (núcleo da M5b rascunho 1, screening.py do commit cfe72ce) e a v0.53 (lebre==0.2.0), nas 64 famílias do E20.
Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit f9906c4, LEBRE054_PROMOVIDA no worktree do commit cfe72ce
e LEBRE053_PROTO como antes):  python -m analises.errata01_v054 FAM ...   |   python -m analises.errata01_v054 resumo
"""
import importlib.util
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

import lebre
from analises import m2_e20 as E20
from analises import m5a_e1 as E

OUT = E.AQUI / "errata01_v054"
COMMIT, PROMOVIDA = "f9906c4", "cfe72ce"
KW054 = dict(m5a=True, m5b=True, m4=True)


def _commit(p):
    head = subprocess.run(["git", "-C", str(p), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(["git", "-C", str(p), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout.strip()
    return head, sujo


def preparar():
    h, s = _commit(E.P54)
    if h != COMMIT or s:
        raise SystemExit(f"LEBRE054_PROTO precisa estar limpo no commit {COMMIT} (encontrado {h})")
    pp = Path(os.environ["LEBRE054_PROMOVIDA"])
    h2, s2 = _commit(pp)
    if h2 != PROMOVIDA or s2:
        raise SystemExit(f"LEBRE054_PROMOVIDA precisa estar limpo no commit {PROMOVIDA} (encontrado {h2})")
    spec = importlib.util.spec_from_file_location("lebre054.screening_promovida", pp / "lebre054" / "screening.py")
    R1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(R1)
    from lebre054.removal import RemovalMixin
    return type("CorePromovida", (RemovalMixin, R1.Core054), {})


def rodar(m, X, y):
    T = len(y); f = np.full(T, np.nan); c = np.zeros(T); ant = 0.0
    for t in range(T):
        yt = None if not math.isfinite(y[t]) else float(y[t])
        f[t] = m.step(X[t], yt).value
        tot = m.cost_per_step * m.n_steps; c[t] = tot - ant; ant = tot
    return f, c, m.cost_per_step


def relatorio(m):
    c = m.core._core
    return {str(u): sorted(c.equivalents(u)) for u in c.active if u[0] == "in"}


def familia(fam):
    CoreP = preparar(); series = []
    for origem, s in E20._series(fam):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); d = X.shape[1]
        kw = dict(season=s.get("season"), season2=s.get("season2"), reference=E.refnome(s))
        e01, prom, v53 = E.Lebre054(d, **kw, **KW054), E.Lebre054(d, **kw, **KW054), lebre.Lebre(d, **kw)
        prom.core._core = CoreP(prom.n_inputs, season=kw["season"], season2=kw["season2"])
        fe, ce, me = rodar(e01, X, y); fp, cp, mp = rodar(prom, X, y); fv, cv, mv = rodar(v53, X, y)
        series.append(dict(serie=s.get("nome"), T=len(y), d=d,
                           identica=bool(np.array_equal(fe, fp, equal_nan=True)), estrutura_igual=e01.structure == prom.structure,
                           relatorio_igual=relatorio(e01) == relatorio(prom), custo_e01=me, custo_prom=mp, custo_v053=mv,
                           pico_e01=float(ce.max()), pico_prom=float(cp.max()), pico_v053=float(cv.max())))
        print(fam, s.get("nome"), {k: v for k, v in series[-1].items() if k != "serie"}, flush=True)
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fam}.json").write_text(json.dumps(dict(familia=fam, commit=COMMIT, promovida=PROMOVIDA, series=series),
                                                indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def resumo():
    R = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8"))["series"] for f in E20.TODAS}
    S = [x for v in R.values() for x in v]
    c1 = all(x["identica"] and x["estrutura_igual"] and x["relatorio_igual"] for x in S)
    c2 = all(abs(x["custo_e01"] - x["custo_prom"]) <= 1e-9 * x["custo_prom"] for x in S)
    linhas, falha3 = [], []
    for f, ss in R.items():
        pe, pp, pv = max(x["pico_e01"] for x in ss), max(x["pico_prom"] for x in ss), max(x["pico_v053"] for x in ss)
        linhas.append(f"| {f} | {len(ss)} | {pv:.0f} | {pp:.0f} | {pe:.0f} | {pe / pv:.3f} |")
        if pe > 1.10 * pv:
            falha3.append(f)
    c3 = not falha3
    L = ["# Errata 01 da v0.54 (M5b rascunho 2): resultado", "",
         f"Plano `ERRATA01_V054_PLANO.md`. Protótipo `{COMMIT}`; v0.54 promovida reproduzida com o núcleo do commit "
         f"`{PROMOVIDA}`; v0.53 = `lebre==0.2.0`. {len(R)} famílias, {len(S)} séries.", "",
         "| Família | séries | pico v0.53 | pico v0.54 promovida | pico v0.54 com errata | errata ÷ v0.53 |",
         "|---|---|---|---|---|---|"]
    L += linhas
    L += ["", f"1. **Identidade com a v0.54 promovida** (previsões, estrutura e relatório): {'atende' if c1 else 'não atende'}",
          f"2. **Custo médio igual ao da promovida:** {'atende' if c2 else 'não atende'}",
          f"3. **Pico ≤ 1,10 × o da v0.53 em cada família:** {'atende' if c3 else 'não atende: ' + ', '.join(falha3)}", "",
          f"**Decisão pela regra do plano:** a errata 01 é **{'aceita' if c1 and c2 and c3 else 'não aceita'}**."]
    (E.AQUI / "ERRATA01_V054_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("feito")


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
