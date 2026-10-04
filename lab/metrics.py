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


def by_group(series):
    """Agrupa os resultados por série pelo campo `grupo`."""
    g = {}
    for r in series:
        g.setdefault(r.get("grupo"), []).append(r)
    return g


def found(r, name):
    """A entrada `name` foi aceita alguma vez nesta série?"""
    return name in r.get("estrutura", {}).get("verdadeiras_aceitas", []) or any(
        e["resultado"] == "accepted" and e["entra"] and e["entra"].split("[")[0] == name for e in r["eventos"])


def accept_time(r, name):
    """Primeiro passo em que `name` foi aceita, ou None."""
    ts = [e["t"] for e in r["eventos"] if e["resultado"] == "accepted" and e["entra"] and e["entra"].split("[")[0] == name]
    return min(ts) if ts else None


def group_table(series, names=None):
    """Resumo por grupo: número de séries, recall médio, séries com entrada falsa aceita, custo e MSE relativos.

    names: entradas cuja taxa de aceitação deve ser reportada (ex. ["x0", "x1"]).
    """
    out = {}
    for g, rs in by_group(series).items():
        st = [r["estrutura"] for r in rs if "estrutura" in r]
        row = dict(n=len(rs), custo_medio=float(np.mean([r["custo_medio"] for r in rs])),
                   us_por_passo=float(np.mean([r["us_por_passo"] for r in rs])))
        if st:
            row["recall_medio"] = float(np.nanmean([x["recall"] for x in st]))
            row["series_com_falsa"] = int(sum(x["falsas_aceitas"] > 0 for x in st))
        for k in sorted({k for r in rs for k in r if k.startswith("mse_rel_")}):
            v = np.array([r.get(k, np.nan) for r in rs], float); v = v[np.isfinite(v) & (v > 0)]
            row[k + "_geo"] = float(np.exp(np.mean(np.log(v)))) if len(v) else np.nan
        for nm in names or []:
            row[f"aceita_{nm}"] = int(sum(found(r, nm) for r in rs))
        out[str(g)] = row
    return out
