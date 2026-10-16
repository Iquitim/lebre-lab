"""D4 da v0.55 (plano: analises/D4_V055_PLANO.md, commitado antes de rodar): variantes A, B7 e B8 do protótipo
lebre-research experiments/LEBRE-V0.55-PROTO-01 (commit 2f250bf) em 15 células sintéticas com sementes novas.

Uso (da raiz do Lab, com LEBRE055_PROTO na pasta do worktree no commit 2f250bf):
  python -m analises.d4_v055 ensaio | sint | resumo
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
OUT = AQUI / "d4_v055"
COMMIT = "2f250bf"
P55 = Path(os.environ["LEBRE055_PROTO"])
sys.path.insert(0, str(P55))
from lebre055.model055 import Lebre055  # noqa: E402

VARIANTES = ("A", "B7", "B8")
SEMENTE_SINT, SEMENTE_ENSAIO, SEMENTE_BOOT = 2026101900, 2026101870, 2026101920
CELULAS = [("N1", 4000, 60), ("N2", 4000, 60), ("N3", 8000, 80), ("N4", 8000, 80), ("N5", 8000, 80),
           ("P1", 8000, 60), ("P2", 8000, 60), ("P3", 8000, 60), ("P4", 8000, 60),
           ("W1", 8000, 40), ("W2", 8000, 40), ("W3", 8000, 40), ("W4", 8000, 40),
           ("P5", 8000, 60), ("P6", 8000, 60)]
PROCS = 14
RETENCAO = ("P1", "P2", "P3", "P5", "P6", "W1", "W3", "W4")


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
    """(X, y, season, reference): células 0-8 com a geração da D1, células W do §1 do plano"""
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
        return ar1(rng, 0.5, T, 4), a + np.sin(2 * np.pi * np.arange(T) / 24), 24, "seasonal"
    if cel in ("W1", "W2", "W3"):
        X = ar1(rng, 0.5, T, 4); e = rng.standard_normal(T); a = np.zeros(T)
        for t in range(1, T):
            a[t] = 0.5 * a[t - 1] + e[t]
        y = a + np.sin(2 * np.pi * np.arange(T) / 24) + (0.0 if cel == "W2" else 0.3 * lag(X[:, 0], 3))
        return X, y, (None if cel == "W3" else 30), ("persistence" if cel == "W3" else "seasonal")
    if cel == "W4":
        c = ar1(rng, 0.95, T, 1)[:, 0]
        y = np.maximum(0.0, np.sin(2 * np.pi * np.arange(T) / 24)) * (1 + 0.3 * c) + 0.05 * rng.standard_normal(T)
        X = np.column_stack([c + 0.3 * rng.standard_normal(T), ar1(rng, 0.5, T, 3)])
        return X, y, 30, "seasonal"
    if cel == "P5":                                            # I(1) com efeito forte e atraso 1 nas diferenças
        X = ar1(rng, 0.5, T, 4)
        return X, np.cumsum(1.0 * lag(X[:, 0], 1) + 0.5 * rng.standard_normal(T)), None, "persistence"
    if cel == "P6":                                            # P3 + três entradas espúrias que passeiam
        X = np.column_stack([ar1(rng, 0.5, T, 1), np.cumsum(rng.standard_normal((T, 3)), 0)])
        return X, np.cumsum(0.5 * lag(X[:, 0], 2) + 0.5 * rng.standard_normal(T)), None, "persistence"
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
                mse=float(np.mean((y[ok] - f[ok]) ** 2)), custo=m.cost_per_step, estrutura=m.structure)


def tarefa(arg):
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
        res = p.map(tarefa, tarefas, chunksize=1)
    nome = "ensaio_sint.json" if ensaio else "sint.json"
    (OUT / nome).write_text(json.dumps(dict(commit=COMMIT, resultados=res), indent=1) + "\n", encoding="utf-8", newline="\n")
    print("sint:", len(res), "séries ->", nome)


def cp_sup(x, n, a=0.05):
    """limite superior de Clopper–Pearson bilateral 95%, por bisseção na binomial"""
    if x >= n:
        return 1.0
    lo, hi = x / n, 1.0
    for _ in range(80):
        p = (lo + hi) / 2
        cdf = sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))
        lo, hi = (p, hi) if cdf > a / 2 else (lo, p)
    return (lo + hi) / 2


def geo_ic(lr, rng, B=4000):
    lr = np.asarray(lr, float)
    bs = lr[rng.integers(0, len(lr), size=(B, len(lr)))].mean(1)
    return float(np.exp(lr.mean())), [float(np.exp(np.quantile(bs, 0.025))), float(np.exp(np.quantile(bs, 0.975)))]


def resumo():
    S = json.loads((OUT / "sint.json").read_text(encoding="utf-8"))["resultados"]
    by = {}
    for r in S:
        by.setdefault(r["celula"], []).append(r)
    out = {"celulas": {}, "criterios": {}}
    for ci, (cel, _, _) in enumerate(CELULAS):
        rs = by[cel]; n = len(rs); c = {}
        for v in VARIANTES:
            fin = sum(bool(r[v]["ext_final"]) for r in rs); ever = sum(bool(r[v]["ext_ever"]) for r in rs)
            x0 = sum(r[v]["x0_final"] for r in rs)
            c[v] = dict(n=n, ext_final=fin, ext_final_sup=cp_sup(fin, n), ext_ever=ever, ext_ever_sup=cp_sup(ever, n),
                        x0_final=x0, x0_frac=x0 / n, isca_ever=sum("x1" in r[v]["ext_ever"] for r in rs),
                        own_past_final=sum("own_past" in r[v]["estrutura"] for r in rs),
                        custo_mediana=float(np.median([r[v]["custo"] for r in rs])))
            if v != "A":
                lr = [math.log(r[v]["mse"] / r["A"]["mse"]) for r in rs]
                c[v]["razao_geo"], c[v]["razao_ic95"] = geo_ic(lr, np.random.default_rng([SEMENTE_BOOT, ci, VARIANTES.index(v)]))
        if cel == "P1":
            for v in VARIANTES[1:]:
                both = [(r["A"]["t_x0"], r[v]["t_x0"]) for r in rs if r["A"]["t_x0"] is not None and r[v]["t_x0"] is not None]
                c[v]["atraso_mediana"] = float(np.median([b for _, b in both])) if both else None
                c[v]["atraso_mediana_A"] = float(np.median([a for a, _ in both])) if both else None
        out["celulas"][cel] = c
    C = out["celulas"]
    for v in ("B7", "B8"):
        cr = {}
        cr["D2-a"] = all(C[x][v]["ext_final_sup"] <= 0.10 for x in ("N1", "N2")) and \
            (C["N1"][v]["ext_final"] + C["N2"][v]["ext_final"] < C["N1"]["A"]["ext_final"] + C["N2"]["A"]["ext_final"])
        cr["D2-b"] = all(C[x][v]["ext_ever_sup"] <= 0.05 for x in ("N3", "N4", "N5"))
        cr["D2-d"] = all(C[x][v]["x0_frac"] >= C[x]["A"]["x0_frac"] - 0.05 for x in RETENCAO)
        p1 = C["P1"][v]
        cr["D2-e"] = p1["atraso_mediana"] is not None and p1["atraso_mediana"] <= 1.5 * p1["atraso_mediana_A"]
        sup = {cel: C[cel][v]["razao_ic95"][1] for cel, _, _ in CELULAS}
        cr["D2-f"] = all(s_ <= 1.02 for s_ in sup.values()); cr["D2-f_piores"] = sorted(sup.items(), key=lambda kv: -kv[1])[:4]
        custos = [r[v]["custo"] / r["A"]["custo"] for r in S]
        cr["D2-g_mediana"] = float(np.median(custos)); cr["D2-g"] = cr["D2-g_mediana"] <= 1.25
        cr["D4-h"] = all(C[x][v]["razao_ic95"][1] < 1.0 for x in ("P3", "P6"))
        p6 = sum(any(u != "x0" for u in r[v]["ext_final"]) for r in by["P6"])
        cr["D4-i_espurias_P6"] = p6; cr["D4-i"] = cp_sup(p6, len(by["P6"])) <= 0.10
        cr["PASSA"] = all(cr[k] for k in ("D2-a", "D2-b", "D2-d", "D2-e", "D2-f", "D2-g", "D4-h", "D4-i"))
        out["criterios"][v] = cr
    (OUT / "resumo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(out["criterios"], indent=1, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "sint":
        sint()
    elif cmd == "ensaio":
        sint(ensaio=True)
    elif cmd == "resumo":
        resumo()
