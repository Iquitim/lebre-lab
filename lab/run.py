"""Executor de cenários.

Uso:  python -m lab.run scenarios/A/A02_exemplo.py
      python -m lab.run scenarios/A/A02_exemplo.py --ensaio   (roda sem registrar; para conferir o cenário)

Um cenário é um arquivo .py com:
  SPEC = dict(id, frente, pergunta, expectativa, criterio, sementes, aquecimento)
  def gerar(semente) -> dict(y, X, season=None, season2=None, truth=None, nome=...)   # uma série por semente
  def avaliar(resumo, series) -> "atende" | "nao_atende" | "inconclusivo"              # o critério, em código
  (gerar pode devolver grupo="..." para o critério avaliar por grupo, ex. por número de entradas)

Regras aplicadas aqui: o cenário e o código comum (lab/) precisam estar commitados; cada execução registrada vira uma
linha em runs/REGISTRO.csv e uma pasta runs/<id>/ com os detalhes.
"""
import csv
import datetime as dt
import importlib.util
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import lebre
from lab.baselines import Naive, OnlineLinear, SeasonalNaive, Zero
from lab.metrics import coverage, forecast_metrics, structure_metrics

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "runs" / "REGISTRO.csv"
FIELDS = ["id", "data", "cenario", "frente", "commit", "versao_lebre", "sementes", "n_series", "criterio", "resultado",
          "resumo", "notas"]


def _git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def check_committed(scenario_path):
    """Recusa rodar se o cenário ou o código comum tiverem alterações não commitadas."""
    rel = [str(Path(scenario_path).resolve().relative_to(ROOT)), "lab"]
    dirty = _git("status", "--porcelain", "--", *rel)
    if dirty:
        raise SystemExit(f"Alterações não commitadas (commite antes de rodar):\n{dirty}")
    return _git("rev-parse", "--short", "HEAD")


def load(path):
    spec = importlib.util.spec_from_file_location("cenario", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for k in ("SPEC", "gerar", "avaliar"):
        if not hasattr(mod, k):
            raise SystemExit(f"cenário sem {k}")
    return mod


def run_series(s, warmup):
    """Roda a LEBRE e os comparadores numa série. Devolve métricas e eventos."""
    y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
    T, d = X.shape
    season = s.get("season")
    models = [Naive(d), OnlineLinear(d)]
    if season:
        models.append(SeasonalNaive(d, season))
    if s.get("zero_baseline"):
        models.append(Zero(d))
    m = lebre.Lebre(d, season=season, season2=s.get("season2"))
    F = {mm.name: np.full(T, np.nan) for mm in models}
    f, lo, hi = np.full(T, np.nan), np.full(T, np.nan), np.full(T, np.nan)
    t0 = time.perf_counter()
    for t in range(T):
        yt = None if not math.isfinite(y[t]) else float(y[t])
        fc = m.step(X[t], yt)
        f[t], lo[t], hi[t] = fc.value, fc.lower, fc.upper
    sec = time.perf_counter() - t0
    start = int(warmup * T) if warmup < 1 else int(warmup)
    for mm in models:
        for t in range(T):
            F[mm.name][t] = mm.predict(X[t]); mm.observe(None if not math.isfinite(y[t]) else float(y[t]))
    res = dict(nome=s.get("nome", ""), grupo=s.get("grupo"), T=T, d=d,
               lebre=forecast_metrics(y, f, start), cobertura=coverage(y, lo, hi, start),
               custo_medio=m.cost_per_step, us_por_passo=sec / T * 1e6,
               previsoes_nao_finitas=int(np.sum(~np.isfinite(f[start:]))),
               comparadores={k: forecast_metrics(y, v, start) for k, v in F.items()},
               estrutura_final=m.structure,
               eventos=[dict(t=e.t, resultado=e.outcome, mudanca=e.change, entra=e.added, sai=e.removed,
                             log_evidencia=e.log_evidence, amostras=e.samples) for e in m.events])
    for k, v in res["comparadores"].items():
        res[f"mse_rel_{k}"] = res["lebre"]["mse"] / v["mse"] if v["mse"] and math.isfinite(v["mse"]) else np.nan
    if s.get("truth") is not None:
        res["estrutura"] = structure_metrics(m.events, m.structure, s["truth"])
    return res


def summarise(per_series):
    """Resumo agregado: medianas e médias geométricas dos MSE relativos, totais de estrutura."""
    out = {"n_series": len(per_series)}
    keys = sorted({k for r in per_series for k in r if k.startswith("mse_rel_")})
    for k in keys:
        v = np.array([r[k] for r in per_series], float); v = v[np.isfinite(v) & (v > 0)]
        out[k + "_geo"] = float(np.exp(np.mean(np.log(v)))) if len(v) else np.nan
    out["cobertura_media"] = float(np.nanmean([r["cobertura"] for r in per_series]))
    out["custo_medio"] = float(np.mean([r["custo_medio"] for r in per_series]))
    out["custo_max_series"] = float(np.max([r["custo_medio"] for r in per_series]))
    st = [r["estrutura"] for r in per_series if "estrutura" in r]
    if st:
        out["recall_medio"] = float(np.nanmean([x["recall"] for x in st]))
        out["falsas_aceitas_total"] = int(sum(x["falsas_aceitas"] for x in st))
        out["series_com_falsa"] = int(sum(x["falsas_aceitas"] > 0 for x in st))
    return out


def _json(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def register(row, details, reg=REG):
    reg.parent.mkdir(parents=True, exist_ok=True)
    new = not reg.exists()
    with open(reg, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    d = reg.parent / row["id"]; d.mkdir(parents=True, exist_ok=True)
    (d / "detalhes.json").write_text(json.dumps(details, indent=1, ensure_ascii=False, default=_json), encoding="utf-8")


def main(argv):
    path, dry = argv[0], "--ensaio" in argv
    mod = load(path); S = mod.SPEC
    commit = "ensaio" if dry else check_committed(path)
    per = [run_series(mod.gerar(seed), S.get("aquecimento", 0.2)) for seed in S["sementes"]]
    resumo = summarise(per)
    resultado = mod.avaliar(resumo, per)
    print(json.dumps(resumo, indent=1, ensure_ascii=False, default=_json)); print("resultado:", resultado)
    if dry:
        print("(ensaio: nada foi registrado)"); return
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    row = dict(id=f"{stamp}_{S['id']}", data=dt.date.today().isoformat(), cenario=S["id"], frente=S["frente"],
               commit=commit, versao_lebre=lebre.__version__, sementes=" ".join(map(str, S["sementes"])),
               n_series=len(per), criterio=S["criterio"], resultado=resultado,
               resumo=json.dumps(resumo, ensure_ascii=False, default=_json), notas=S.get("notas", ""))
    register(row, dict(spec=S, resumo=resumo, series=per))
    print("registrado:", row["id"])


if __name__ == "__main__":
    main(sys.argv[1:])
