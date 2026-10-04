"""Geradores sintéticos compartilhados pela Frente A."""
import numpy as np


def ar1(rng, T, d, phi=0.5):
    """d entradas AR(1) independentes, variância 1."""
    e = rng.standard_normal((T, d)) * np.sqrt(1 - phi ** 2)
    x = np.empty((T, d)); x[0] = rng.standard_normal(d)
    for t in range(1, T):
        x[t] = phi * x[t - 1] + e[t]
    return x


def lag(v, k):
    """v atrasado de k passos (zeros no início)."""
    out = np.zeros_like(v)
    if k == 0:
        return v.copy()
    out[k:] = v[:-k]
    return out


def base_truth(rng, T, d, noise=0.7, phi=0.5):
    """Cenário de referência: y_t = 0.7 x0_{t-3} + 0.5 x1_{t-10} + ruído (desvio `noise`); demais entradas irrelevantes.

    Atrasos >= 1 de propósito: o valor atual das entradas (atraso 0) já entra no modelo base da LEBRE sem nenhuma
    decisão, então um efeito de atraso 0 não deixaria rastro nas métricas de estrutura.
    """
    X = ar1(rng, T, d, phi)
    y = 0.7 * lag(X[:, 0], 3) + 0.5 * lag(X[:, 1], 10) + noise * rng.standard_normal(T)
    return X, y
