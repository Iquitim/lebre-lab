"""Comparadores online e causais. Cada um tem a mesma interface da LEBRE: predict(x) e depois observe(y).

y = None ou NaN marca um alvo faltante; entradas faltantes (NaN) são trocadas pelo último valor visto.
"""
import math

import numpy as np


class _Base:
    name = "base"

    def __init__(self, n_inputs):
        self.d = n_inputs
        self.hist = []                                   # alvos observados (NaN quando faltam)

    def _last(self, k=1):
        """k-ésimo alvo observado mais recente que não é NaN, ou NaN."""
        seen = 0
        for v in reversed(self.hist):
            if not math.isnan(v):
                seen += 1
                if seen == k:
                    return v
        return math.nan

    def observe(self, y):
        self.hist.append(math.nan if y is None or (isinstance(y, float) and math.isnan(y)) else float(y))


class Zero(_Base):
    """Prevê sempre zero (referência para retornos financeiros)."""
    name = "zero"

    def predict(self, x):
        return 0.0


class Naive(_Base):
    """Prevê o último valor observado."""
    name = "ingenuo"

    def predict(self, x):
        return self._last()


class SeasonalNaive(_Base):
    """Prevê o valor de uma estação atrás (cai para o ingênuo enquanto não há uma estação de histórico)."""
    name = "sazonal_ingenuo"

    def __init__(self, n_inputs, season):
        super().__init__(n_inputs)
        self.s = int(season)

    def predict(self, x):
        if len(self.hist) >= self.s and not math.isnan(self.hist[-self.s]):
            return self.hist[-self.s]
        return self._last()


class OnlineLinear(_Base):
    """Regressão linear online (RLS com esquecimento) com defasagens do alvo e das entradas.

    Variáveis: 1, y_{t-1..p}, x_t, x_{t-1..q} (as entradas atuais são conhecidas no momento da previsão, como na LEBRE).
    """
    name = "linear_online"

    def __init__(self, n_inputs, p=2, q=8, lam=0.999, delta=100.0):
        super().__init__(n_inputs)
        self.p, self.q, self.lam = p, q, lam
        self.k = 1 + p + n_inputs * (q + 1)
        self.w = np.zeros(self.k)
        self.P = np.eye(self.k) * delta
        self.xhist = []                                  # entradas (já com NaN preenchido)
        self._z = None

    def _features(self, x):
        x = np.asarray(x, float).copy()
        if self.xhist:
            bad = ~np.isfinite(x)
            x[bad] = self.xhist[-1][bad]
        x[~np.isfinite(x)] = 0.0
        self.xhist.append(x)
        ys = [self._last(i) for i in range(1, self.p + 1)]
        ys = [0.0 if math.isnan(v) else v for v in ys]
        xs = [self.xhist[-1 - j] if len(self.xhist) > j else np.zeros(self.d) for j in range(self.q + 1)]
        return np.concatenate([[1.0], ys, *xs])

    def predict(self, x):
        self._z = self._features(x)
        return float(self.w @ self._z)

    def observe(self, y):
        super().observe(y)
        v = self.hist[-1]
        if math.isnan(v):
            return
        z = self._z
        Pz = self.P @ z
        g = Pz / (self.lam + z @ Pz)
        self.w = self.w + g * (v - self.w @ z)
        self.P = (self.P - np.outer(g, Pz)) / self.lam
