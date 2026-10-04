"""Testa o código comum (comparadores, métricas, executor e registro). Não é um experimento: não registra nada."""
import csv
import math

import numpy as np
import pytest

from lab.baselines import Naive, OnlineLinear, SeasonalNaive, Zero
from lab.metrics import coverage, forecast_metrics, structure_metrics
from lab.run import FIELDS, register, run_series, summarise


def _toy(T=4000, seed=0):
    rng = np.random.default_rng(seed); X = rng.standard_normal((T, 2))
    y = 0.8 * np.r_[np.zeros(3), X[:-3, 0]] + 0.3 * rng.standard_normal(T)
    return dict(nome="toy", y=y, X=X, season=None, truth=dict(relevant=["x0"]))


def test_baselines_are_causal_and_handle_gaps():
    n, s = Naive(1), SeasonalNaive(1, 3)
    for v in [1.0, 2.0, None, 4.0]:
        n.predict([0.0]); n.observe(v)
        s.predict([0.0]); s.observe(v)
    assert n.predict([0.0]) == 4.0                       # último observado
    assert s.predict([0.0]) == 2.0                       # 3 passos atrás (o faltante não conta como valor)
    assert Zero(1).predict([1.0]) == 0.0


def test_online_linear_learns_a_lagged_input():
    s = _toy(); m = OnlineLinear(2); f = []
    for t in range(len(s["y"])):
        f.append(m.predict(s["X"][t])); m.observe(s["y"][t])
    e = forecast_metrics(s["y"], f, 1000)
    assert e["mse"] < 0.2                                # ruído 0.09; sem o x0 seria ~0.73


def test_metrics():
    assert forecast_metrics([1, 2, np.nan], [1, 1, 5], 0) == dict(mse=0.5, mae=0.5, n=2)
    assert coverage([0, 0, 5], [-1, -1, -1], [1, 1, 1], 0) == pytest.approx(2 / 3)


def test_run_series_and_structure():
    r = run_series(_toy(), 0.2)
    assert r["lebre"]["n"] > 0 and math.isfinite(r["lebre"]["mse"])
    assert {"ingenuo", "linear_online"} <= set(r["comparadores"])
    assert r["estrutura"]["recall"] == 1.0 and r["estrutura"]["verdadeiras_aceitas"] == ["x0"]
    s = summarise([r, r]); assert s["n_series"] == 2 and s["recall_medio"] == 1.0


def test_structure_metrics_counts_false_and_ignores_internal():
    class E:                                              # evento mínimo no formato da biblioteca
        def __init__(self, t, added): self.t, self.outcome, self.added = t, "accepted", added
    ev = [E(10, "own_past"), E(20, "x1"), E(30, "x0[1-3]")]
    m = structure_metrics(ev, ["x0[1-3]", "x1", "own_past"], dict(relevant=["x0"]))
    assert m["falsas_aceitas"] == 1 and m["primeira_falsa"] == 20 and m["tempo_deteccao"] == {"x0": 30}
    assert m["finais_falsas"] == ["x1"]


def test_register_appends_and_never_overwrites(tmp_path):
    reg = tmp_path / "REGISTRO.csv"
    row = {k: "x" for k in FIELDS}
    register(dict(row, id="r1"), {"a": 1}, reg); register(dict(row, id="r2"), {"a": np.float64(2)}, reg)
    rows = list(csv.DictReader(open(reg, encoding="utf-8")))
    assert [r["id"] for r in rows] == ["r1", "r2"] and (tmp_path / "r2" / "detalhes.json").exists()
