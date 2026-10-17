"""Banco fixo da v0.55 (plano: analises/BANCO_V055_PLANO.md, commitado antes de qualquer rodada nele).

23 células sintéticas com verdade conhecida, medidas e critérios **fixos** para todas as rodadas de desenvolvimento e
para a confirmação final. Uma rodada nova só acrescenta uma entrada em RODADAS (commit do protótipo, sementes,
variantes), num commit anterior à sua execução.

Uso (da raiz do Lab, com LEBRE055_PROTO na pasta do worktree do commit da rodada):
  python -m analises.banco_v055 <rodada> ensaio | sint | resumo
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
P55 = Path(os.environ.get("LEBRE055_PROTO", "."))

# rodadas: cada uma registrada (em commit próprio) antes de rodar
RODADAS = {
    "D5": dict(commit="b0522a0", base=2026102000, ensaio=2026101950, boot=2026102030, variantes=("A", "B9", "B10"),
               candidatas=("B9", "B10")),
}

T_CURTO, T_LONGO = 4000, 8000
CELULAS = [  # (nome, T, n)
    ("N1", T_CURTO, 60), ("N2", T_CURTO, 60), ("N3", T_LONGO, 80), ("N4", T_LONGO, 80), ("N5", T_LONGO, 80),
    ("P1", T_LONGO, 60), ("P2", T_LONGO, 60), ("P3", T_LONGO, 60), ("P4", T_LONGO, 60), ("P5", T_LONGO, 60),
    ("P6", T_LONGO, 60), ("W1", T_LONGO, 40), ("W2", T_LONGO, 40), ("W3", T_LONGO, 40), ("W4", T_LONGO, 40),
    ("Q1", T_LONGO, 40), ("Q2", T_LONGO, 40), ("Q3", T_LONGO, 40), ("Q4", T_LONGO, 40), ("Q5", T_LONGO, 40),
    ("Q6", T_LONGO, 40), ("Q7", T_LONGO, 40), ("Q8", T_LONGO, 40)]
VERDADEIRAS = {"P1": ["x0"], "P2": ["x0"], "P3": ["x0"], "P5": ["x0"], "P6": ["x0"], "W1": ["x0"], "W3": ["x0"],
               "W4": ["x0"], "Q1": ["x0"], "Q2": ["x0"], "Q3": ["x0"], "Q4": ["x0"], "Q5": ["x0", "x1"], "Q6": ["x0"],
               "Q7": ["x0"], "Q8": ["x0"]}
ESPURIAS_Q7 = [f"x{i}" for i in range(4, 10)]          # passeios independentes da Q7
INTEGRADAS_COM_ENTRADA = ("P3", "P5", "P6", "Q1", "Q4", "Q5", "Q6", "Q7")
PROCS = 14


def ar1(rng, rho, n, d):
    e = rng.standard_normal((n, d)) * math.sqrt(1 - rho ** 2); z = np.zeros((n, d)); z[0] = rng.standard_normal(d)
    for t in range(1, n):
        z[t] = rho * z[t - 1] + e[t]
    return z


def lag(v, k):
    return np.r_[np.zeros(k), v[:-k]]


def _ar(rng, rho, T, scale=1.0):
    e = scale * rng.standard_normal(T); a = np.zeros(T)
    for t in range(1, T):
        a[t] = rho * a[t - 1] + e[t]
    return a


def gerar(cel, T, rng):
    """(X, y, season, reference) de cada célula (tabela do §1 do plano)"""
    tt = np.arange(T)
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
        a = _ar(rng, 0.5, T)
        return ar1(rng, 0.5, T, 4), a + np.sin(2 * np.pi * tt / 24), 24, "seasonal"
    if cel in ("W1", "W2", "W3"):
        X = ar1(rng, 0.5, T, 4); a = _ar(rng, 0.5, T)
        y = a + np.sin(2 * np.pi * tt / 24) + (0.0 if cel == "W2" else 0.3 * lag(X[:, 0], 3))
        return X, y, (None if cel == "W3" else 30), ("persistence" if cel == "W3" else "seasonal")
    if cel == "W4":
        c = ar1(rng, 0.95, T, 1)[:, 0]
        y = np.maximum(0.0, np.sin(2 * np.pi * tt / 24)) * (1 + 0.3 * c) + 0.05 * rng.standard_normal(T)
        return np.column_stack([c + 0.3 * rng.standard_normal(T), ar1(rng, 0.5, T, 3)]), y, 30, "seasonal"
    if cel == "P5":
        X = ar1(rng, 0.5, T, 4)
        return X, np.cumsum(1.0 * lag(X[:, 0], 1) + 0.5 * rng.standard_normal(T)), None, "persistence"
    if cel == "P6":
        X = np.column_stack([ar1(rng, 0.5, T, 1), np.cumsum(rng.standard_normal((T, 3)), 0)])
        return X, np.cumsum(0.5 * lag(X[:, 0], 2) + 0.5 * rng.standard_normal(T)), None, "persistence"
    if cel == "Q1":                                    # integrada sazonal com entrada nas diferenças
        X = ar1(rng, 0.5, T, 4)
        y = np.cumsum(0.5 * lag(X[:, 0], 2) + 0.5 * rng.standard_normal(T)) + np.sin(2 * np.pi * tt / 24)
        return X, y, 24, "seasonal"
    if cel == "Q2":                                    # AR(2) forte com entrada
        X = ar1(rng, 0.5, T, 4); e = 0.3 * rng.standard_normal(T); d_ = 0.3 * lag(X[:, 0], 3); y = np.zeros(T)
        for t in range(2, T):
            y[t] = 1.2 * y[t - 1] - 0.35 * y[t - 2] + d_[t] + e[t]
        return X, y, None, "persistence"
    if cel == "Q3":                                    # estacionária na 1ª metade, integrada na 2ª
        X = ar1(rng, 0.5, T, 4); h = T // 2
        a = _ar(rng, 0.5, h, 0.3) + 0.3 * lag(X[:, 0], 3)[:h]
        b = a[-1] + np.cumsum(0.5 * lag(X[:, 0], 2)[h:] + 0.5 * rng.standard_normal(T - h))
        return X, np.r_[a, b], None, "persistence"
    if cel == "Q4":                                    # integrada com relação intermitente nas diferenças
        X = ar1(rng, 0.5, T, 4); on = np.ones(T); on[3000:5500] = 0.0
        return X, np.cumsum(on * 0.5 * lag(X[:, 0], 2) + 0.5 * rng.standard_normal(T)), None, "persistence"
    if cel == "Q5":                                    # duas entradas verdadeiras nas diferenças
        X = ar1(rng, 0.5, T, 4)
        return X, np.cumsum(0.4 * lag(X[:, 0], 2) + 0.3 * lag(X[:, 1], 5) + 0.5 * rng.standard_normal(T)), None, "persistence"
    if cel == "Q6":                                    # caudas pesadas
        X = ar1(rng, 0.5, T, 4)
        return X, np.cumsum(0.5 * lag(X[:, 0], 2) + 0.3 * rng.standard_t(3, T)), None, "persistence"
    if cel == "Q7":                                    # 10 entradas: verdadeira, 3 iscas correlacionadas, 6 passeios
        x0 = ar1(rng, 0.5, T, 1)[:, 0]
        iscas = 0.7 * x0[:, None] + 0.71 * ar1(rng, 0.5, T, 3)
        X = np.column_stack([x0, iscas, np.cumsum(rng.standard_normal((T, 6)), 0)])
        return X, np.cumsum(0.5 * lag(x0, 2) + 0.5 * rng.standard_normal(T)), None, "persistence"
    if cel == "Q8":                                    # quase integrada com entrada no nível
        X = ar1(rng, 0.5, T, 4); e = 0.5 * rng.standard_normal(T); d_ = 0.3 * lag(X[:, 0], 3); y = np.zeros(T)
        for t in range(1, T):
            y[t] = 0.99 * y[t - 1] + d_[t] + e[t]
        return X, y, None, "persistence"
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


def proto_info(commit):
    c = subprocess.run(["git", "-C", str(P55), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(["git", "-C", str(P55), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if c != commit or sujo.strip():
        raise SystemExit(f"exige o protótipo limpo no commit {commit} (encontrado {c})")


def medir(m, y, f):
    ext_final = sorted(u for u in m.structure if u.startswith("x"))
    acc = [e for e in m.events if e.outcome == "accepted" and e.change in ("add", "swap") and e.added and e.added.startswith("x")]
    t_x0 = next((e.t for e in acc if e.added == "x0"), None)
    T = len(y); ok = np.isfinite(y) & np.isfinite(f); ok[: T // 3] = False
    return dict(ext_final=ext_final, ext_ever=sorted({e.added for e in acc}), t_x0=t_x0,
                mse=float(np.mean((y[ok] - f[ok]) ** 2)), custo=m.cost_per_step, estrutura=m.structure)


def tarefa(arg):
    c, k, base, variantes = arg
    sys.path.insert(0, str(P55))
    from lebre055.model055 import Lebre055
    cel, T, _ = CELULAS[c]
    X, y, season, ref = gerar(cel, T, np.random.default_rng([base + c, k]))
    out = dict(celula=cel, k=k)
    for v in variantes:
        m = Lebre055(X.shape[1], season=season, reference=ref, variant=v)
        f = np.array([m.step(X[t], float(y[t])).value for t in range(T)])
        out[v] = medir(m, y, f)
    return out


def sint(rod, ensaio=False):
    R = RODADAS[rod]; proto_info(R["commit"])
    out = AQUI / f"banco_v055_{rod}"; out.mkdir(exist_ok=True)
    base = R["ensaio"] if ensaio else R["base"]
    tarefas = [(c, k, base, R["variantes"]) for c, (_, _, n) in enumerate(CELULAS) for k in range(1 if ensaio else n)]
    with Pool(PROCS) as p:
        res = p.map(tarefa, tarefas, chunksize=1)
    nome = "ensaio_sint.json" if ensaio else "sint.json"
    (out / nome).write_text(json.dumps(dict(rodada=rod, **{k: v for k, v in R.items() if k != "variantes"},
                                            variantes=list(R["variantes"]), resultados=res), indent=1) + "\n",
                            encoding="utf-8", newline="\n")
    print(rod, "sint:", len(res), "séries ->", nome)


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


def geo_ic(grupos, rng, B=4000):
    """média geométrica das razões e IC 95% por bootstrap estratificado (reamostra séries dentro de cada célula)"""
    grupos = [np.asarray(g, float) for g in grupos]
    pt = float(np.exp(np.concatenate(grupos).mean()))
    bs = np.zeros(B)
    for g in grupos:
        bs += g[rng.integers(0, len(g), size=(B, len(g)))].sum(1)
    bs /= sum(len(g) for g in grupos)
    return pt, [float(np.exp(np.quantile(bs, 0.025))), float(np.exp(np.quantile(bs, 0.975)))]


def resumo(rod):
    R = RODADAS[rod]; V = R["variantes"]
    out_dir = AQUI / f"banco_v055_{rod}"
    S = json.loads((out_dir / "sint.json").read_text(encoding="utf-8"))["resultados"]
    by = {}
    for r in S:
        by.setdefault(r["celula"], []).append(r)
    out = {"celulas": {}, "criterios": {}}
    for ci, (cel, _, _) in enumerate(CELULAS):
        rs = by[cel]; n = len(rs); c = {}
        for v in V:
            fin = sum(bool(r[v]["ext_final"]) for r in rs); ever = sum(bool(r[v]["ext_ever"]) for r in rs)
            ver = VERDADEIRAS.get(cel, [])
            ret = sum(u in r[v]["ext_final"] for r in rs for u in ver)
            c[v] = dict(n=n, ext_final=fin, ext_final_sup=cp_sup(fin, n), ext_ever=ever, ext_ever_sup=cp_sup(ever, n),
                        retencao=ret, retencao_frac=ret / (n * len(ver)) if ver else None,
                        own_past_final=sum("own_past" in r[v]["estrutura"] for r in rs),
                        custo_mediana=float(np.median([r[v]["custo"] for r in rs])))
            if cel == "Q7":
                c[v]["passeios_final"] = sum(any(u in ESPURIAS_Q7 for u in r[v]["ext_final"]) for r in rs)
                c[v]["iscas_final"] = sum(any(u in ("x1", "x2", "x3") for u in r[v]["ext_final"]) for r in rs)
            if v != "A":
                lr = [math.log(r[v]["mse"] / r["A"]["mse"]) for r in rs]
                c[v]["razao_geo"], c[v]["razao_ic95"] = geo_ic([lr], np.random.default_rng([R["boot"], ci, V.index(v)]))
        if cel == "P1":
            for v in V[1:]:
                both = [(r["A"]["t_x0"], r[v]["t_x0"]) for r in rs if r["A"]["t_x0"] is not None and r[v]["t_x0"] is not None]
                c[v]["atraso_mediana"] = float(np.median([b for _, b in both])) if both else None
                c[v]["atraso_mediana_A"] = float(np.median([a for a, _ in both])) if both else None
        out["celulas"][cel] = c
    C = out["celulas"]
    for v in V[1:]:
        cr = {}
        cr["C-a"] = all(C[x][v]["ext_final_sup"] <= 0.10 for x in ("N1", "N2")) and \
            (C["N1"][v]["ext_final"] + C["N2"][v]["ext_final"] < C["N1"]["A"]["ext_final"] + C["N2"]["A"]["ext_final"]) and \
            cp_sup(C["Q7"][v]["passeios_final"], C["Q7"][v]["n"]) <= 0.10
        cr["C-b"] = all(C[x][v]["ext_ever_sup"] <= 0.05 for x in ("N3", "N4", "N5"))
        cr["C-d_falhas"] = [x for x in VERDADEIRAS if C[x][v]["retencao_frac"] < C[x]["A"]["retencao_frac"] - 0.05]
        cr["C-d"] = not cr["C-d_falhas"]
        p1 = C["P1"][v]
        cr["C-e"] = p1["atraso_mediana"] is not None and p1["atraso_mediana"] <= 1.5 * p1["atraso_mediana_A"]
        sup = {cel: C[cel][v]["razao_ic95"][1] for cel, _, _ in CELULAS}
        cr["C-f_falhas"] = {k: round(s_, 4) for k, s_ in sup.items() if s_ > 1.02}
        cr["C-f"] = not cr["C-f_falhas"]
        custos = [r[v]["custo"] / r["A"]["custo"] for r in S]
        cr["C-g_mediana"] = float(np.median(custos)); cr["C-g"] = cr["C-g_mediana"] <= 1.25
        grupos = [[math.log(r[v]["mse"] / r["A"]["mse"]) for r in by[x]] for x in INTEGRADAS_COM_ENTRADA]
        cr["C-h_conjunto"], cr["C-h_conjunto_ic95"] = geo_ic(grupos, np.random.default_rng([R["boot"], 99, V.index(v)]))
        cr["C-h"] = C["P3"][v]["razao_ic95"][1] < 1.0 and C["P6"][v]["razao_ic95"][1] < 1.0 and cr["C-h_conjunto_ic95"][1] < 1.0
        cr["PASSA"] = all(cr[k] for k in ("C-a", "C-b", "C-d", "C-e", "C-f", "C-g", "C-h"))
        out["criterios"][v] = cr
    (out_dir / "resumo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(out["criterios"], indent=1, ensure_ascii=False))


if __name__ == "__main__":
    rod, cmd = sys.argv[1], sys.argv[2]
    if cmd == "sint":
        sint(rod)
    elif cmd == "ensaio":
        sint(rod, ensaio=True)
    elif cmd == "resumo":
        resumo(rod)
