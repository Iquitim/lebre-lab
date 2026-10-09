"""E13 (plano: diagnosticos/E13_PLANO.md): utilidades comuns. Só descrição."""
import math

import numpy as np

from analises import m1_val4 as Y
from analises import m2_dev as M
from analises import m2_dev_r6 as R6
from analises import m2_val2 as V2
from analises import m2_val3 as X
from lab.baselines import Naive, SeasonalNaive, Zero
from lab.run import ROOT, load

ARQ = dict(M.ARQ) | dict(R6.ARQ_V) | dict(V2.ARQ) | dict(X.ARQ) | dict(Y.ARQ)
import importlib
M.CLIP_K_M1 = importlib.import_module(M.Lebre053.__module__.rsplit(".", 1)[0] + ".precisao").CLIP_K
KW = dict(porta=True, eps_porta=0.002, recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod")


def series(fam):
    mod = load(ROOT / "scenarios" / ARQ[fam])
    for i in mod.SPEC["sementes"]:
        try:
            yield mod.gerar(i)
        except IndexError:
            return


def refnome(s):
    return "zero" if s.get("zero_baseline") else ("sazonal" if s.get("season") else "persistencia")


def rastrear(s, precisao=False):
    """Roda M2 (com ou sem M1) passo a passo e devolve os sinais internos por passo."""
    y, X_ = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X_.shape
    m = M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), referencia=refnome(s), precisao=precisao, **KW)
    cols = ("out", "R", "L", "L52", "D", "M", "s", "wD_L", "wM_L", "e", "sE", "corte")
    tr = {c: np.full(T, np.nan) for c in cols}
    for t in range(T):
        f = m.predict(X_[t])
        tr["out"][t] = f.value; tr["R"][t] = m._R; tr["L"][t] = m._L; tr["L52"][t] = m._L52
        if m._R_def and m._d is not None:
            tr["D"][t] = m._d; tr["M"][t] = m._m; tr["s"][t] = m.agregador.s()
            tr["wD_L"][t] = m._subD.pesos()[1]; tr["wM_L"][t] = m._subM.pesos()[1]
        p = m.precisao
        if p is not None and getattr(p, "e", None) is not None:
            tr["e"][t] = p.e; tr["sE"][t] = p.prod.s()
            B = M.CLIP_K_M1 * max(math.sqrt(p.e2_52), p._piso) if p.e2_52 is not None else math.nan
            tr["corte"][t] = float(abs(p.e - m._L52) >= B * (1 - 1e-9)) if math.isfinite(B) else math.nan
        m.observe(None if not math.isfinite(y[t]) else float(y[t]))
    return y, tr, m
