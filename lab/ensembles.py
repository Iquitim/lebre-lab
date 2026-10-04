"""Ensembles construídos em volta da LEBRE congelada (Frente D). A biblioteca não é alterada: os membros são instâncias
comuns de lebre.Lebre (ou comparadores), e a combinação é feita aqui.

Todos os modelos têm a interface predict(x) -> float e observe(y), e um atributo `custo` (operações por passo,
quando conhecido).
"""
import math

import numpy as np

import lebre


class LebreW:
    """Uma LEBRE como membro: opcionalmente vê só algumas entradas (`cols`) e declara seus próprios ciclos."""

    def __init__(self, d, cols=None, season=None, season2=None, name="lebre"):
        self.cols = list(range(d)) if cols is None else list(cols)
        self.m = lebre.Lebre(len(self.cols), season=season, season2=season2)
        self.name = name

    def predict(self, x):
        return self.m.predict(np.asarray(x, float)[self.cols]).value

    def observe(self, y):
        self.m.observe(y)

    @property
    def custo(self):
        return self.m.cost_per_step


class Media:
    """Média simples das previsões dos membros (ignora membros sem previsão)."""

    def __init__(self, membros, name):
        self.membros, self.name = membros, name

    def predict(self, x):
        p = np.array([m.predict(x) for m in self.membros], float)
        ok = np.isfinite(p)
        return float(p[ok].mean()) if ok.any() else math.nan

    def observe(self, y):
        for m in self.membros:
            m.observe(y)

    @property
    def custo(self):
        return sum(getattr(m, "custo", 0.0) or 0.0 for m in self.membros)


class PesosOnline(Media):
    """Combinação com pesos proporcionais ao inverso do erro quadrático recente de cada membro (média exponencial).

    Começa com pesos iguais; um membro sem previsão num passo fica de fora desse passo.
    """

    def __init__(self, membros, name, alpha=0.01):
        super().__init__(membros, name)
        self.alpha = alpha
        self.e2 = np.full(len(membros), np.nan)
        self._p = None

    def pesos(self):
        if np.isnan(self.e2).all():
            return np.ones(len(self.membros)) / len(self.membros)
        e = np.where(np.isnan(self.e2), np.nanmax(self.e2), self.e2)
        w = 1.0 / np.maximum(e, 1e-12)
        return w / w.sum()

    def predict(self, x):
        self._p = np.array([m.predict(x) for m in self.membros], float)
        ok = np.isfinite(self._p)
        if not ok.any():
            return math.nan
        w = self.pesos() * ok
        return float(np.sum(w[ok] * self._p[ok]) / w.sum())

    def observe(self, y):
        if y is not None and math.isfinite(y) and self._p is not None:
            err = (y - self._p) ** 2
            for k in range(len(self.membros)):
                if math.isfinite(err[k]):
                    self.e2[k] = err[k] if math.isnan(self.e2[k]) else (1 - self.alpha) * self.e2[k] + self.alpha * err[k]
        super().observe(y)
