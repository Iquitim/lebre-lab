"""Medição M5A_E1 (plano: analises/M5A_E1_PLANO.md): M5a da v0.54 (rascunho 0, revisão a) contra a v0.53 (lebre==0.2.0).

Precisa de: LEBRE054_PROTO = pasta experiments/LEBRE-V0.54-PROTO-01 de uma cópia fixa do lebre-research (git worktree);
LEBRE053_PROTO = pasta do protótipo da v0.53 (só para os carregadores do E20); lebre==0.2.0 instalada.
Uso (da raiz do Lab):
  python -m analises.m5a_e1 custo | cenarios | familias FAM ... | resumo
"""
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

import lebre
from analises import m2_dev as M
from analises import m2_e20 as E20
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

if lebre.__version__ != "0.2.0":
    raise SystemExit(f"M5A_E1 exige lebre==0.2.0 (encontrada {lebre.__version__})")
P54 = Path(os.environ["LEBRE054_PROTO"])
sys.path.insert(0, str(P54))
from lebre054.model054 import Lebre054  # noqa: E402

AQUI = ROOT / "analises"
OUT = AQUI / "m5a_e1"
SEMENTE_BOOT = 20261060
SEM_3A = list(range(20261070, 20261090))
SEM_3B = list(range(20261090, 20261110))


def proto_info():
    sujo = subprocess.run(["git", "-C", str(P54), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if sujo.strip():
        raise SystemExit(f"protótipo da v0.54 com alterações não commitadas:\n{sujo}")
    commit = subprocess.run(["git", "-C", str(P54), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    return dict(commit=commit, dormancy_sha256=hashlib.sha256((P54 / "lebre054" / "dormancy.py").read_bytes()).hexdigest())


def refnome(s):
    return "zero" if s.get("zero_baseline") else ("seasonal" if s.get("season") else "persistence")


def par(s, track=None):
    """Roda v0.53 e v0.54 na série; devolve previsões, objetos e (opcional) trilhas por passo."""
    y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
    T, d = X.shape
    kw = dict(season=s.get("season"), season2=s.get("season2"), reference=refnome(s))
    a, b = lebre.Lebre(d, **kw), Lebre054(d, **kw)
    fa, fb = np.full(T, np.nan), np.full(T, np.nan)
    w53, sono = np.zeros(T), np.zeros(T, bool)
    for t in range(T):
        yt = None if not math.isfinite(y[t]) else float(y[t])
        fa[t] = a.step(X[t], yt).value; fb[t] = b.step(X[t], yt).value
        if track:
            w53[t] = a.layer_weights["m1"]; sono[t] = b._m1.dormant
    return y, fa, fb, a, b, w53, sono


def mse(y, f, ini, fim=None):
    s = slice(ini, fim)
    ok = np.isfinite(y[s]) & np.isfinite(f[s])
    return float(np.mean((y[s][ok] - f[s][ok]) ** 2))


def geo(v):
    v = np.asarray(v, float); v = v[np.isfinite(v) & (v > 0)]
    return float(np.exp(np.mean(np.log(v)))) if len(v) else float("nan")


# ------------------------------------------------------------------ 1. custo
def custo():
    info = proto_info(); res = {"prototipo": info}
    for cen, arq in (("A01", "A/A01_muitas_entradas.py"), ("A05", "A/A05_mudanca_regime.py"), ("C03", "C/C03_niveis_de_preco.py")):
        mod = load(ROOT / "scenarios" / arq); rows = []
        for sd in mod.SPEC["sementes"]:
            s = mod.gerar(sd)
            y, fa, fb, a, b, _, _ = par(s)
            ini = int(0.2 * len(y))
            rows.append(dict(serie=s.get("nome"), m1_v053=a._m1.fp / a.n_steps, m1_v054=b._m1.fp / b.n_steps,
                             total_v053=a.cost_per_step, total_v054=b.cost_per_step, sono=b.m1_state,
                             mse_v054_sobre_v053=mse(y, fb, ini) / mse(y, fa, ini)))
            print(cen, rows[-1]["serie"], round(rows[-1]["m1_v053"]), "->", round(rows[-1]["m1_v054"]), flush=True)
        m53, m54 = np.mean([r["m1_v053"] for r in rows]), np.mean([r["m1_v054"] for r in rows])
        res[cen] = dict(series=rows, m1_v053=m53, m1_v054=m54, razao=m54 / m53, atende=bool(m54 <= 0.25 * m53),
                        total_v053=float(np.mean([r["total_v053"] for r in rows])),
                        total_v054=float(np.mean([r["total_v054"] for r in rows])))
    OUT.mkdir(exist_ok=True)
    (OUT / "custo.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# ------------------------------------------------------------------ 2 e 5. famílias do E20
def familia(fam):
    info = proto_info()
    curtas = fam in E20.CURTAS
    series, reps = [], []
    for k, (origem, s) in enumerate(E20._series(fam)):
        y, fa, fb, a, b, _, _ = par(s)
        T = len(y); ini = int(0.2 * T)
        L = E20.bloco_curta(origem) if curtas else E20.bloco(fam)
        rng = np.random.default_rng([SEMENTE_BOOT, E20.TODAS.index(fam), k])
        p, rep = M.par_bootstrap(y, fb, fa, ini, L, rng)
        reps.append(rep)
        st = b.m1_state
        series.append(dict(serie=s.get("nome"), origem=origem, T=T, razao=p, sono=st,
                           nan_aval=int((np.isfinite(y) & ~np.isfinite(fb))[ini:].sum()),
                           identica=bool(np.array_equal(fa, fb, equal_nan=True)),
                           m1_v053=a._m1.fp / a.n_steps if a._m1 else None, m1_v054=st["m1_fp_per_step"],
                           total_v053=a.cost_per_step, total_v054=b.cost_per_step))
        print(fam, s.get("nome"), "razão", round(p, 5), "dormiu", st["sleeps"], "idêntica", series[-1]["identica"], flush=True)
    logs = np.array([math.log(r["razao"]) for r in series])
    rr = np.vstack(reps).mean(0); rr = rr[np.isfinite(rr)]
    resumo = dict(geo=float(np.exp(logs.mean())), ic95=[float(np.exp(np.quantile(rr, 0.025))), float(np.exp(np.quantile(rr, 0.975)))],
                  n=len(series), nan_aval=int(sum(r["nan_aval"] for r in series)),
                  dormiram=int(sum(r["sono"]["sleeps"] > 0 for r in series)),
                  identidade_ok=all(r["identica"] for r in series if r["sono"]["sleeps"] == 0))
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fam}.json").write_text(json.dumps(dict(familia=fam, prototipo=info, semente=SEMENTE_BOOT, resumo=resumo,
                                                     series=series), indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
    print(fam, "resumo", resumo, flush=True)


# ------------------------------------------------------------------ 3a e 3b. cenários
def _entradas(rng, T):
    e = rng.standard_normal((T, 4)) * math.sqrt(1 - 0.36); X = np.zeros((T, 4))
    for t in range(1, T):
        X[t] = 0.6 * X[t - 1] + e[t]
    return X


def _lag(v, k):
    return np.r_[np.zeros(k), v[:-k]]


def gerar_3a(sd):
    rng = np.random.default_rng(sd); T = 30000; X = _entradas(rng, T); e = rng.standard_normal(T); y = np.zeros(T)
    drive = 0.6 * np.mean([_lag(X[:, 0], k) for k in (2, 3)], 0) + 0.4 * np.mean([_lag(X[:, 1], k) for k in range(4, 8)], 0)
    for t in range(T):
        y[t] = 0.8 * (X[t - 3, 0] if t >= 3 else 0.0) + 0.6 * e[t] if t < 15000 else \
            1.2 * y[t - 1] - 0.35 * y[t - 2] + drive[t] + 0.3 * e[t]
    return dict(nome=f"s{sd}", y=y, X=X)


def gerar_3b(sd):
    rng = np.random.default_rng(sd); T = 36000; X = _entradas(rng, T); e = rng.standard_normal(T); y = np.zeros(T)
    drive = 0.6 * np.mean([_lag(X[:, 0], k) for k in (2, 3)], 0) + 0.4 * np.mean([_lag(X[:, 1], k) for k in range(4, 8)], 0)
    for t in range(2, T):
        y[t] = y[t - 1] + 0.5 * e[t] if 12000 <= t < 24000 else 1.2 * y[t - 1] - 0.35 * y[t - 2] + drive[t] + 0.3 * e[t]
    return dict(nome=f"s{sd}", y=y, X=X)


def cenarios():
    info = proto_info(); res = {"prototipo": info}
    rows = []
    for sd in SEM_3A:
        y, fa, fb, a, b, _, _ = par(gerar_3a(sd))
        rows.append(dict(serie=sd, razao_pos=mse(y, fb, 15000) / mse(y, fa, 15000), sono=b.m1_state,
                         nan=int((~np.isfinite(fb)).sum())))
        print("3a", sd, round(rows[-1]["razao_pos"], 4), rows[-1]["sono"], flush=True)
    g = geo([r["razao_pos"] for r in rows])
    res["3a"] = dict(series=rows, geo_pos=g, atende=bool(g <= 1.02))
    rows = []
    for sd in SEM_3B:
        y, fa, fb, a, b, w53, sono = par(gerar_3b(sd), track=True)
        volta53 = bool((w53[24000:] > 0.5).any())
        dormiu = bool(sono[:24000].any())
        despertou = bool(dormiu and (~sono[24000:]).any() and sono[23999])
        rows.append(dict(serie=sd, razao_ultimo=mse(y, fb, 24000) / mse(y, fa, 24000), v053_volta=volta53,
                         v054_dormiu_antes=dormiu, v054_dormindo_em_24000=bool(sono[23999]), v054_despertou=despertou,
                         sono=b.m1_state, nan=int((~np.isfinite(fb)).sum())))
        print("3b", sd, rows[-1], flush=True)
    cond = [r for r in rows if r["v053_volta"] and r["v054_dormiu_antes"]]
    frac = (sum(r["v054_despertou"] or not r["v054_dormindo_em_24000"] for r in cond) / len(cond)) if cond else float("nan")
    g = geo([r["razao_ultimo"] for r in rows])
    res["3b"] = dict(series=rows, n_condicao=len(cond), fracao_desperta=frac, geo_ultimo=g,
                     despertar="inconclusivo" if len(cond) < 5 else ("atende" if frac >= 0.9 else "nao_atende"),
                     erro_atende=bool(g <= 1.02))
    OUT.mkdir(exist_ok=True)
    (OUT / "cenarios.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


# ------------------------------------------------------------------ resumo
def resumo():
    L = ["# Medição M5A_E1: resultado", "", "Plano `M5A_E1_PLANO.md`.", ""]
    c = json.loads((OUT / "custo.json").read_text(encoding="utf-8"))
    L += [f"Protótipo: commit `{c['prototipo']['commit']}`.", "", "## 1. Custo da M1 (FP por passo)", "",
          "| Cenário | v0.53 | v0.54 | razão | critério (≤ 0,25) | total v0.53 | total v0.54 |", "|---|---|---|---|---|---|---|"]
    for k in ("A01", "A05", "C03"):
        r = c[k]
        L.append(f"| {k} | {r['m1_v053']:.0f} | {r['m1_v054']:.0f} | {r['razao']:.3f} | {'atende' if r['atende'] else 'não atende'} | {r['total_v053']:.0f} | {r['total_v054']:.0f} |")
    fams = [f for f in E20.TODAS if (OUT / f"{f}.json").exists()]
    F = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8"))["resumo"] for f in fams}
    pior = max(F.items(), key=lambda kv: kv[1]["ic95"][1])
    L += ["", f"## 2. Sem piora nas famílias do E20 ({len(F)} de {len(E20.TODAS)})", "",
          f"- famílias com limite superior > 1,01: {[f for f, r in F.items() if r['ic95'][1] > 1.01]}",
          f"- maior limite superior: {pior[0]} {pior[1]['ic95'][1]:.4f} (razão {pior[1]['geo']:.4f})",
          f"- previsões não finitas: {sum(r['nan_aval'] for r in F.values())}",
          f"- séries em que a M1 dormiu: {sum(r['dormiram'] for r in F.values())} de {sum(r['n'] for r in F.values())}",
          f"- identidade onde nunca dormiu: {'ok' if all(r['identidade_ok'] for r in F.values()) else 'FALHOU'}"]
    cc = json.loads((OUT / "cenarios.json").read_text(encoding="utf-8"))
    L += ["", "## 3a. Troca de regime", "", f"- MSE depois da troca, v0.54 ÷ v0.53 (geo, 20): {cc['3a']['geo_pos']:.4f} → "
          f"{'atende' if cc['3a']['atende'] else 'não atende'}",
          "", "## 3b. Útil → inútil → útil", "",
          f"- séries na condição (v0.53 volta a pesar e a v0.54 dormiu antes): {cc['3b']['n_condicao']}",
          f"- fração que desperta: {cc['3b']['fracao_desperta']} → {cc['3b']['despertar']}",
          f"- MSE do último trecho, v0.54 ÷ v0.53 (geo, 20): {cc['3b']['geo_ultimo']:.4f} → "
          f"{'atende' if cc['3b']['erro_atende'] else 'não atende'}"]
    (AQUI / "M5A_E1_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "custo":
        custo()
    elif cmd == "cenarios":
        cenarios()
    elif cmd == "familias":
        for f in sys.argv[2:] or E20.TODAS:
            familia(f)
    elif cmd == "resumo":
        resumo()
