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


def test_synth_and_group_helpers():
    from lab.metrics import accept_time, by_group, found
    from lab.synth import ar1, base_truth, lag
    rng = np.random.default_rng(1); x = ar1(rng, 20000, 2)
    assert abs(x.var() - 1) < 0.1 and abs(np.corrcoef(x[1:, 0], x[:-1, 0])[0, 1] - 0.5) < 0.05
    assert list(lag(np.arange(5.0), 2)) == [0, 0, 0, 1, 2]
    X, y = base_truth(rng, 1000, 4); assert X.shape == (1000, 4) and y.shape == (1000,)
    r = dict(grupo="a", eventos=[dict(t=5, resultado="accepted", entra="x2[1-3]")])
    assert found(r, "x2") and accept_time(r, "x2") == 5 and not found(r, "x0")
    assert list(by_group([r, dict(r, grupo="b")])) == ["a", "b"]


def test_online_linear_is_stable_on_long_series():
    """Regressão do problema de 2026-10-04: sem simetrizar P, o RLS divergia perto de 25 mil passos."""
    from lab.synth import ar1, lag
    rng = np.random.default_rng(601); T = 40000
    X = ar1(rng, T, 2); y = np.cos(2 * np.pi * np.arange(T) / 30000) * lag(X[:, 0], 3) + 0.6 * rng.standard_normal(T)
    m = OnlineLinear(2); f = np.empty(T)
    for t in range(T):
        f[t] = m.predict(X[t]); m.observe(y[t])
    e = (y - f) ** 2
    assert e[-5000:].mean() < 0.6 and np.allclose(m.P, m.P.T)


def test_ensembles_combine_and_weight():
    from lab.ensembles import LebreW, Media, PesosOnline

    class Const:
        def __init__(self, v): self.v, self.name, self.custo = v, f"c{v}", 1.0
        def predict(self, x): return self.v
        def observe(self, y): pass

    m = Media([Const(1.0), Const(3.0), Const(math.nan)], "media")
    assert m.predict([0]) == 2.0 and m.custo == 3.0
    w = PesosOnline([Const(0.0), Const(10.0)], "pesos", alpha=0.5)
    for _ in range(20):
        w.predict([0]); w.observe(0.0)                    # o membro que acerta (0) ganha quase todo o peso
    assert w.pesos()[0] > 0.99 and abs(w.predict([0])) < 0.1
    s = _toy(3000); lw = LebreW(2, cols=[0]); f = []
    for t in range(3000):
        f.append(lw.predict(s["X"][t])); lw.observe(s["y"][t])
    assert np.isfinite(f[-1]) and lw.custo > 0


def test_run_series_reports_extras():
    from lab.ensembles import LebreW, Media
    s = _toy(3000); s["extras"] = [lambda d: Media([LebreW(d, cols=[0], name="a"), LebreW(d, cols=[1], name="b")], "ens")]
    r = run_series(s, 0.2)
    e = r["extras"]["ens"]
    assert math.isfinite(e["mse_rel_lebre"]) and e["custo_rel_lebre"] > 0 and "mse_rel_linear_online" in e


def test_summary_with_heterogeneous_baselines():
    """Regressão de 2026-10-04 (D03): séries com e sem sazonal ingênuo no mesmo cenário quebravam o resumo."""
    from lab.metrics import group_table
    a = dict(grupo="g", custo_medio=1.0, us_por_passo=1.0, cobertura=0.9, mse_rel_ingenuo=0.5, mse_rel_sazonal_ingenuo=0.4)
    b = dict(grupo="g", custo_medio=1.0, us_por_passo=1.0, cobertura=0.9, mse_rel_ingenuo=0.5)
    s = summarise([a, b]); assert s["mse_rel_sazonal_ingenuo_geo"] == pytest.approx(0.4)
    assert group_table([a, b])["g"]["mse_rel_sazonal_ingenuo_geo"] == pytest.approx(0.4)


def test_reserve_of_v053_is_refused():
    from lab import fontes as F
    from lab.reserva import USINAS, SerieReservada, checar_usina
    with pytest.raises(SerieReservada):
        F.ons_carga([2026])
    with pytest.raises(SerieReservada):
        F.fred("DEXUSUK")
    with pytest.raises(SerieReservada):
        F.open_meteo(-23.55, -46.63, "2026-01-01", "2026-02-01", ["temperature_2m"])
    with pytest.raises(SerieReservada):
        checar_usina(sorted(USINAS)[0])
    checar_usina("Conj. Janaúba")                         # usina usada no Lab: liberada


def test_reserve_of_v054_is_refused():
    from lab import fontes as F
    from lab.reserva import _R54, SerieReservada, checar_usina
    with pytest.raises(SerieReservada):
        F.ons_fator([2026])
    for serie in ("DFII10", "DGS1MO", "DHHNGSP"):
        with pytest.raises(SerieReservada):
            F.fred(serie)
    with pytest.raises(SerieReservada):
        checar_usina(_R54["usinas_eolicas"][0])
