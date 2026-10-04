"""Métricas de previsão, de estrutura (quando a verdade é conhecida) e de custo."""
import numpy as np


def forecast_metrics(y, f, start):
    """MSE e MAE a partir do passo `start`, só onde há alvo e previsão."""
    y, f = np.asarray(y, float)[start:], np.asarray(f, float)[start:]
    ok = np.isfinite(y) & np.isfinite(f)
    if not ok.any():
        return dict(mse=np.nan, mae=np.nan, n=0)
    e = y[ok] - f[ok]
    return dict(mse=float(np.mean(e ** 2)), mae=float(np.mean(np.abs(e))), n=int(ok.sum()))


def coverage(y, lo, hi, start):
    y, lo, hi = (np.asarray(a, float)[start:] for a in (y, lo, hi))
    ok = np.isfinite(y) & np.isfinite(lo) & np.isfinite(hi)
    return float(np.mean((y[ok] >= lo[ok]) & (y[ok] <= hi[ok]))) if ok.any() else np.nan


def structure_metrics(events, final_structure, truth):
    """Compara as decisões da LEBRE com a verdade de um cenário sintético.

    truth: dict(relevant=[nomes de entradas verdadeiras, ex. "x0"], changes=[(passo, entrada que passa a valer), ...]).
    Entradas internas (own_past, residual_state) não contam como verdadeiras nem falsas.
    """
    rel = set(truth.get("relevant", []))
    internal = ("own_past", "residual_state")
    acc = [e for e in events if e.outcome == "accepted"]

    def base(u):
        return None if u is None else u.split("[")[0]

    added = [(e.t, base(e.added)) for e in acc if e.added and base(e.added) not in internal]
    true_first = {}
    for t, u in added:
        if u in rel and u not in true_first:
            true_first[u] = t
    false_adds = [(t, u) for t, u in added if u not in rel]
    final = {base(u) for u in final_structure if base(u) not in internal}
    return dict(
        verdadeiras_aceitas=sorted(true_first), n_verdadeiras=len(rel),
        recall=len(true_first) / len(rel) if rel else np.nan,
        falsas_aceitas=len(false_adds), primeira_falsa=false_adds[0][0] if false_adds else None,
        tempo_deteccao={u: t for u, t in true_first.items()},
        estrutura_final=sorted(final), finais_falsas=sorted(final - rel),
    )
