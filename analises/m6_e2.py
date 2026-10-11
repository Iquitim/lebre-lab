"""Medição M6_E2 (plano: analises/M6_E2_PLANO.md): M6 rascunho 1 (protótipo no commit 18906c2). Cópia de m6_e1.py com o
commit, a pasta de saída e a semente trocados.
Por série: (a) argumentos do E20, m6=False contra m6=True; (b) se a série tem ciclo declarado, m6=True sem ciclo e sem
referência declarados, contra (a) sem M6; (c) se não tem, os ciclos aceitos em (a) com M6.
Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit 18906c2 e LEBRE053_PROTO como antes):
  python -m analises.m6_e2 FAM ...   |   python -m analises.m6_e2 resumo
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
OUT = E.AQUI / "m6_e2"
COMMIT = "18906c2"
SEMENTE_BOOT = 20261343
SINTETICAS = [f"A{k:02d}" for k in range(1, 13)]


def proto_info():
    sujo = subprocess.run(["git", "-C", str(E.P54), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if sujo.strip():
        raise SystemExit(f"protótipo da v0.54 com alterações não commitadas:\n{sujo}")
    commit = subprocess.run(["git", "-C", str(E.P54), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    if commit != COMMIT:
        raise SystemExit(f"M6_E2 exige o protótipo no commit {COMMIT} (encontrado {commit})")
    return dict(commit=commit, cycle_sha256=hashlib.sha256((E.P54 / "lebre054" / "cycle.py").read_bytes()).hexdigest())


def rodar(m, X, y):
    f = np.full(len(y), np.nan)
    for t in range(len(y)):
        yt = None if not math.isfinite(y[t]) else float(y[t])
        f[t] = m.step(X[t], yt).value
    return f


def ciclos(m):
    c = m.core._core
    return dict(ciclos=c.cycles, aceitos=[(e[0], e[3][1]) for e in c.events if e[1] == "accepted" and e[2] == "cycle"])


def familia(fam):
    info = proto_info(); curtas = fam in E20.CURTAS
    series, reps_a, reps_b = [], [], []
    for k, (origem, s) in enumerate(E20._series(fam)):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape; ini = int(0.2 * T)
        kw = dict(season=s.get("season"), season2=s.get("season2"), reference=E.refnome(s))
        L = E20.bloco_curta(origem) if curtas else E20.bloco(fam)
        a, b = Lebre054(d, **kw), Lebre054(d, m6=True, **kw)
        fa, fb = rodar(a, X, y), rodar(b, X, y)
        pa, ra = M.par_bootstrap(y, fb, fa, ini, L, np.random.default_rng([SEMENTE_BOOT, E20.TODAS.index(fam), k, 0]))
        reps_a.append(ra)
        r = dict(serie=s.get("nome"), origem=origem, T=T, d=d, ciclo_declarado=[kw["season"], kw["season2"]],
                 razao_a=pa, nan_aval=int((np.isfinite(y) & ~np.isfinite(fb))[ini:].sum()),
                 identica_a=bool(np.array_equal(fa, fb, equal_nan=True)), m6_a=ciclos(b),
                 custo_sem=a.cost_per_step, custo_com=b.cost_per_step)
        if kw["season"]:
            c = Lebre054(d, m6=True, reference="zero" if kw["reference"] == "zero" else None)
            fc = rodar(c, X, y)
            pb, rb = M.par_bootstrap(y, fc, fa, ini, L, np.random.default_rng([SEMENTE_BOOT, E20.TODAS.index(fam), k, 1]))
            reps_b.append(rb)
            r.update(razao_b=pb, m6_b=ciclos(c), referencia_b=c.reference, nan_b=int((np.isfinite(y) & ~np.isfinite(fc))[ini:].sum()),
                     custo_b=c.cost_per_step)
        else:
            r.update(razao_b=None)
        series.append(r)
        print(fam, s.get("nome"), "a", round(pa, 5), r["m6_a"]["ciclos"], "b", r["razao_b"] and round(r["razao_b"], 4),
              r.get("m6_b", {}).get("ciclos"), flush=True)

    def resumo_de(chave, reps):
        v = [x[chave] for x in series if x.get(chave) is not None and np.isfinite(x[chave]) and x[chave] > 0]
        if not v:
            return None
        rr = np.vstack(reps).mean(0); rr = rr[np.isfinite(rr)]
        return dict(geo=float(np.exp(np.mean(np.log(v)))), ic95=[float(np.exp(np.quantile(rr, 0.025))),
                                                                 float(np.exp(np.quantile(rr, 0.975)))], n=len(v))
    resumo = dict(a=resumo_de("razao_a", reps_a), b=resumo_de("razao_b", reps_b) if reps_b else None,
                  nan_aval=int(sum(x["nan_aval"] for x in series)), n=len(series),
                  com_ciclo_aceito_a=int(sum(bool(x["m6_a"]["aceitos"]) for x in series)),
                  custo_sem=float(np.mean([x["custo_sem"] for x in series])), custo_com=float(np.mean([x["custo_com"] for x in series])))
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fam}.json").write_text(json.dumps(dict(familia=fam, prototipo=info, semente=SEMENTE_BOOT, resumo=resumo,
                                                     series=series), indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
    print(fam, "resumo", resumo, flush=True)


def resumo():
    R = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8")) for f in E20.TODAS}
    c1 = all(r["resumo"]["a"]["ic95"][1] <= 1.01 and r["resumo"]["nan_aval"] == 0 for r in R.values())
    pior = max(R.items(), key=lambda kv: kv[1]["resumo"]["a"]["ic95"][1])
    d02 = {f: R[f]["resumo"]["b"]["geo"] for f in ("B01", "B02")}
    c2 = all(v <= 1.05 for v in d02.values())
    falso_a02 = R["A02"]["resumo"]["com_ciclo_aceito_a"]
    sint = [x for f in SINTETICAS for x in R[f]["series"]]
    falso_sint = sum(bool(x["m6_a"]["aceitos"]) for x in sint)
    c3 = falso_a02 == 0 and falso_sint <= 0.05 * len(sint)
    L = ["# Medição M6_E2 (M6 rascunho 1): resultado", "",
         f"Plano `M6_E2_PLANO.md`. Protótipo no commit `{COMMIT}`; {len(R)} famílias do E20.", "",
         "| Família | séries | (a) com M6 ÷ sem M6, ciclo como no E20 | IC 95% | (b) sem declarar com M6 ÷ declarado sem M6 | IC 95% | séries com ciclo aceito em (a) | custo sem → com |",
         "|---|---|---|---|---|---|---|---|"]
    for f, r in R.items():
        z = r["resumo"]; b = z["b"]
        L.append(f"| {f} | {z['n']} | {z['a']['geo']:.4f} | {z['a']['ic95'][0]:.4f}–{z['a']['ic95'][1]:.4f} | "
                 + (f"{b['geo']:.4f} | {b['ic95'][0]:.4f}–{b['ic95'][1]:.4f}" if b else "— | —")
                 + f" | {z['com_ciclo_aceito_a']} | {z['custo_sem']:.0f} → {z['custo_com']:.0f} |")
    L += ["", f"1. **Sem piora com o ciclo declarado** (limite superior ≤ 1,01; pior: {pior[0]}, "
              f"{pior[1]['resumo']['a']['ic95'][1]:.4f}): {'atende' if c1 else 'não atende'}",
          f"2. **Sem declarar, D02** (B01 {d02['B01']:.4f}; B02 {d02['B02']:.4f}; limite 1,05): {'atende' if c2 else 'não atende'}",
          f"3. **Nenhum ciclo falso** (A02: {falso_a02} séries; A01 a A12: {falso_sint} de {len(sint)}, limite 5%): "
          f"{'atende' if c3 else 'não atende'}", "",
          f"**Decisão pela regra do plano:** a M6 (rascunho 1) **{'segue para validação em dados novos' if c1 and c2 and c3 else 'não segue'}**."]
    (E.AQUI / "M6_E2_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("feito")


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
