"""D1 da v0.55 (plano: analises/D1_V055_PLANO.md, commitado antes de rodar): variantes A, B4 e B5 do protótipo
lebre-research experiments/LEBRE-V0.55-PROTO-01 (commit 324d667) em 9 células sintéticas e nas 64 famílias do E20.

Uso (da raiz do Lab, com LEBRE055_PROTO, LEBRE054_PROTO e LEBRE053_PROTO nas pastas do worktree no commit 324d667):
  python -m analises.d1_v055 sint | e20 | resumo | ensaio
"""
import json
import math
import os
import subprocess
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
OUT = AQUI / "d1_v055"
COMMIT = "324d667"
P55 = Path(os.environ["LEBRE055_PROTO"])
sys.path.insert(0, str(P55))
from lebre055.model055 import Lebre055  # noqa: E402

VARIANTES = ("A", "B4", "B5")
SEMENTE_SINT, SEMENTE_ENSAIO, SEMENTE_BOOT = 2026101600, 2026101590, 2026101610
CELULAS = [("N1", 4000, 60), ("N2", 4000, 60), ("N3", 8000, 80), ("N4", 8000, 80), ("N5", 8000, 80),
           ("P1", 8000, 60), ("P2", 8000, 60), ("P3", 8000, 60), ("P4", 8000, 60)]
PROCS = 14


def proto_info():
    commit = subprocess.run(["git", "-C", str(P55), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(["git", "-C", str(P55), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if commit != COMMIT or sujo.strip():
        raise SystemExit(f"exige o protótipo limpo no commit {COMMIT} (encontrado {commit})")
    return commit


def ar1(rng, rho, n, d):
    e = rng.standard_normal((n, d)) * math.sqrt(1 - rho ** 2); z = np.zeros((n, d)); z[0] = rng.standard_normal(d)
    for t in range(1, n):
        z[t] = rho * z[t - 1] + e[t]
    return z


def lag(v, k):
    return np.r_[np.zeros(k), v[:-k]]


def gerar(cel, T, rng):
    """(X, y, season, reference) da célula, como na tabela do §1 do plano"""
    if cel == "N1":
        return np.cumsum(rng.standard_normal((T, 5)), 0), np.cumsum(rng.standard_normal(T)), None, "persistence"
    if cel == "N2":
        y = np.cumsum(rng.standard_normal(T)); return ar1(rng, 0.95, T, 5), y, None, "persistence"
    if cel in ("N3", "N5"):
        e = rng.standard_normal(T)
        if cel == "N5":
            e[T // 2:] *= 3.0
        y = np.zeros(T)
        for t in range(1, T):
            y[t] = 0.8 * y[t - 1] + e[t]
        return ar1(rng, 0.5, T, 4), y, None, "persistence"
    if cel == "N4":
        e = rng.standard_normal(T); a = np.zeros(T)
        for t in range(1, T):
            a[t] = 0.5 * a[t - 1] + e[t]
        y = a + np.sin(2 * np.pi * np.arange(T) / 24)
        return ar1(rng, 0.5, T, 4), y, 24, "seasonal"
    X = ar1(rng, 0.5, T, 4)
    if cel == "P1":
        return X, 0.3 * lag(X[:, 0], 3) + 0.3 * rng.standard_normal(T), None, "persistence"
    if cel == "P2":
        X[:, 1] = 0.7 * X[:, 0] + 0.71 * ar1(rng, 0.5, T, 1)[:, 0]
        return X, 0.3 * lag(X[:, 0], 3) + 0.3 * rng.standard_normal(T), None, "persistence"
    if cel == "P3":
        return X, np.cumsum(0.5 * lag(X[:, 0], 2) + 0.5 * rng.standard_normal(T)), None, "persistence"
    if cel == "P4":
        X[:, 0] = np.cumsum(rng.standard_normal(T)); X[:, 1:] = np.cumsum(rng.standard_normal((T, 3)), 0)
        return X, X[:, 0] + ar1(rng, 0.5, T, 1)[:, 0], None, "persistence"
    raise ValueError(cel)


def medir(m, y, f):
    ext_final = sorted(u for u in m.structure if u.startswith("x"))
    acc = [e for e in m.events if e.outcome == "accepted" and e.change in ("add", "swap") and e.added and e.added.startswith("x")]
    t_x0 = next((e.t for e in acc if e.added == "x0"), None)
    T = len(y); ok = np.isfinite(y) & np.isfinite(f); ok[: T // 3] = False
    return dict(ext_final=ext_final, ext_ever=sorted({e.added for e in acc}), t_x0=t_x0, x0_final="x0" in ext_final,
                mse=float(np.mean((y[ok] - f[ok]) ** 2)), custo=m.cost_per_step)


def tarefa_sint(arg):
    c, k, base = arg
    cel, T, _ = CELULAS[c]
    X, y, season, ref = gerar(cel, T, np.random.default_rng([base + c, k]))
    out = dict(celula=cel, k=k)
    for v in VARIANTES:
        m = Lebre055(X.shape[1], season=season, reference=ref, variant=v)
        f = np.array([m.step(X[t], float(y[t])).value for t in range(T)])
        out[v] = medir(m, y, f)
    return out


def sint(ensaio=False):
    proto_info(); OUT.mkdir(exist_ok=True)
    base = SEMENTE_ENSAIO if ensaio else SEMENTE_SINT
    tarefas = [(c, k, base) for c, (_, _, n) in enumerate(CELULAS) for k in range(1 if ensaio else n)]
    with Pool(PROCS) as p:
        res = p.map(tarefa_sint, tarefas, chunksize=1)
    nome = "ensaio_sint.json" if ensaio else "sint.json"
    (OUT / nome).write_text(json.dumps(dict(commit=COMMIT, resultados=res), indent=1) + "\n", encoding="utf-8", newline="\n")
    print("sint:", len(res), "séries ->", OUT / nome)


def tarefa_e20(fam):
    from analises import m2_dev as M
    from analises import m2_e20 as E20
    curtas = fam in E20.CURTAS; fi = E20.TODAS.index(fam)
    series, reps = [], {v: [] for v in VARIANTES[1:]}
    for k, (origem, s) in enumerate(E20._series(fam)):
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape; ini = int(0.2 * T)
        ref = "zero" if s.get("zero_baseline") else ("seasonal" if s.get("season") else "persistence")
        kw = dict(season=s.get("season"), season2=s.get("season2"), reference=ref)
        fs, ms = {}, {}
        for v in VARIANTES:
            m = Lebre055(d, **kw, variant=v); f = np.full(T, np.nan)
            for t in range(T):
                f[t] = m.step(X[t], None if not math.isfinite(y[t]) else float(y[t])).value
            fs[v], ms[v] = f, m
        L = E20.bloco_curta(origem) if curtas else E20.bloco(fam)
        row = dict(serie=s.get("nome"), T=T, custo={v: ms[v].cost_per_step for v in VARIANTES},
                   ext_final={v: sorted(u for u in ms[v].structure if u.startswith("x")) for v in VARIANTES},
                   nan={v: int((np.isfinite(y) & ~np.isfinite(fs[v]))[ini:].sum()) for v in VARIANTES})
        for vi, v in enumerate(VARIANTES[1:], start=1):
            p, rep = M.par_bootstrap(y, fs[v], fs["A"], ini, L, np.random.default_rng([SEMENTE_BOOT, fi, k, vi]))
            row[f"razao_{v}"] = p; reps[v].append(rep)
        series.append(row)
    resumo = {}
    for v in VARIANTES[1:]:
        logs = [math.log(x[f"razao_{v}"]) for x in series if np.isfinite(x[f"razao_{v}"]) and x[f"razao_{v}"] > 0]
        rr = np.vstack(reps[v]).mean(0); rr = rr[np.isfinite(rr)]
        resumo[v] = dict(geo=float(np.exp(np.mean(logs))), ic95=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))],
                         custo_mediana=float(np.median([x["custo"][v] / x["custo"]["A"] for x in series])))
    return dict(familia=fam, n=len(series), resumo=resumo, series=series)


def e20(ensaio=False):
    proto_info(); OUT.mkdir(exist_ok=True)
    from analises import m2_e20 as E20
    fams = E20.TODAS[:1] if ensaio else list(E20.TODAS)
    with Pool(PROCS) as p:
        res = p.map(tarefa_e20, fams, chunksize=1)
    nome = "ensaio_e20.json" if ensaio else "e20.json"
    (OUT / nome).write_text(json.dumps(dict(commit=COMMIT, familias=res), indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8", newline="\n")
    print("e20:", len(res), "famílias ->", OUT / nome)


def cp_sup(x, n, a=0.05):
    """limite superior de Clopper–Pearson bilateral 95%, por bisseção na binomial (sem dependências novas)"""
    if x >= n:
        return 1.0
    lo, hi = x / n, 1.0
    for _ in range(80):
        p = (lo + hi) / 2
        cdf = sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))
        lo, hi = (p, hi) if cdf > a / 2 else (lo, p)
    return (lo + hi) / 2


def resumo():
    S = json.loads((OUT / "sint.json").read_text(encoding="utf-8"))["resultados"]
    F = json.loads((OUT / "e20.json").read_text(encoding="utf-8"))["familias"]
    by = {}
    for r in S:
        by.setdefault(r["celula"], []).append(r)
    out = {"celulas": {}, "criterios": {}}
    for cel, rs in by.items():
        n = len(rs); c = {}
        for v in VARIANTES:
            fin = sum(bool(r[v]["ext_final"]) for r in rs); ever = sum(bool(r[v]["ext_ever"]) for r in rs)
            x0 = sum(r[v]["x0_final"] for r in rs)
            c[v] = dict(n=n, ext_final=fin, ext_final_sup=cp_sup(fin, n), ext_ever=ever, ext_ever_sup=cp_sup(ever, n), x0_final=x0,
                        x0_frac=x0 / n, isca_ever=sum("x1" in r[v]["ext_ever"] for r in rs),
                        mse_geo=float(np.exp(np.mean([math.log(r[v]["mse"]) for r in rs]))),
                        custo_mediana=float(np.median([r[v]["custo"] for r in rs])))
        if cel == "P1":
            for v in VARIANTES[1:]:
                both = [(r["A"]["t_x0"], r[v]["t_x0"]) for r in rs if r["A"]["t_x0"] is not None and r[v]["t_x0"] is not None]
                c[v]["atraso_mediana"] = float(np.median([b for _, b in both])) if both else None
                c[v]["atraso_mediana_A"] = float(np.median([a for a, _ in both])) if both else None
                c[v]["atraso_n"] = len(both)
        out["celulas"][cel] = c
    for v in VARIANTES[1:]:
        C = out["celulas"]; cr = {}
        cr["D1-a"] = all(C[x][v]["ext_final_sup"] <= 0.10 for x in ("N1", "N2")) and \
            (C["N1"][v]["ext_final"] + C["N2"][v]["ext_final"] < C["N1"]["A"]["ext_final"] + C["N2"]["A"]["ext_final"])
        cr["D1-b"] = all(C[x][v]["ext_ever_sup"] <= 0.05 for x in ("N3", "N4", "N5"))
        cr["D1-d"] = all(C[x][v]["x0_frac"] >= C[x]["A"]["x0_frac"] - 0.05 for x in ("P1", "P2"))
        p1 = C["P1"][v]
        cr["D1-e"] = p1["atraso_mediana"] is not None and p1["atraso_mediana"] <= 1.5 * p1["atraso_mediana_A"]
        sup = {f["familia"]: f["resumo"][v]["ic95"][1] for f in F}
        cr["D1-f"] = all(s <= 1.02 for s in sup.values()); cr["D1-f_piores"] = sorted(sup.items(), key=lambda kv: -kv[1])[:5]
        custos = [x["custo"][v] / x["custo"]["A"] for f in F for x in f["series"]]
        cr["D1-g"] = float(np.median(custos)) <= 1.25; cr["D1-g_mediana"] = float(np.median(custos))
        cr["nan"] = int(sum(x["nan"][v] for f in F for x in f["series"]))
        cr["PASSA"] = all(cr[k] for k in ("D1-a", "D1-b", "D1-d", "D1-e", "D1-f", "D1-g"))
        out["criterios"][v] = cr
    niv = {}
    for f in F:
        if f["familia"].endswith("C03"):
            niv[f["familia"]] = {v: sum(bool(x["ext_final"][v]) for x in f["series"]) for v in VARIANTES} | {"n": f["n"]}
    out["niveis_C03"] = niv
    (OUT / "resumo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(out["criterios"], indent=1, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "sint":
        sint()
    elif cmd == "e20":
        e20()
    elif cmd == "ensaio":
        sint(ensaio=True); e20(ensaio=True)
    elif cmd == "resumo":
        resumo()
