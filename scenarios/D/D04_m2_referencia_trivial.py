"""D04: protótipo da mudança M2 da v0.53 (partir da referência trivial e só se afastar com evidência), em volta da
LEBRE congelada. Nota de desenho 01 da v0.53, seção M2; diagnóstico F9 (diagnosticos/F9_CONCLUSAO.md)."""
from pathlib import Path

import numpy as np

from lab.baselines import Naive, SeasonalNaive, Zero
from lab.ensembles import LebreW, PesosOnline, Porta
from lab.run import load

ROOT = Path(__file__).resolve().parents[2]
CEN = {c: load(ROOT / "scenarios" / p) for c, p in [("C01", "C/C01_retornos.py"), ("C03", "C/C03_niveis_de_preco.py"),
                                                   ("C04", "C/C04_juros.py"), ("B01", "B/B01_solar.py"),
                                                   ("B02", "B/B02_carga_eletrica.py")]}
SERIES = [(c, i) for c, m in CEN.items() for i in m.SPEC["sementes"]]
NEGATIVOS, POSITIVOS = ("C01", "C03", "C04"), ("B01", "B02")

SPEC = dict(
    id="D04",
    frente="D",
    pergunta="Um protótipo de M2 (a previsão parte da referência trivial e só usa a LEBRE enquanto ela erra menos) "
             "elimina a perda contra a referência nos testes negativos sem piorar onde a LEBRE já é boa?",
    expectativa="Nos testes negativos (retornos, níveis, juros) a porta deve ficar quase sempre na referência e chegar "
                "a ~1% dela. Na carga e na solar a LEBRE erra muito menos que o sazonal ingênuo, então a porta deve "
                "ficar quase sempre na LEBRE; a perda deve vir só do início (antes de a evidência se formar). A versão "
                "por pesos deve perder mais na carga e na solar, porque a referência ruim sempre leva algum peso.",
    criterio="Versão 'porta' (declarada antes como a que decide): em cada família negativa (C01, C03, C04), MSE da porta "
             "÷ MSE da referência (média geométrica) <= 1,01; em cada família positiva (B01, B02), MSE da porta ÷ MSE da "
             "LEBRE (média geométrica) <= 1,02. As margens de 1% e 2% são as margens de empate.",
    sementes=list(range(len(SERIES))),
    aquecimento=0.2,
    notas="Referência: zero (C01, C04), passeio aleatório (C03), sazonal ingênuo (B01, B02). Porta: média exponencial "
          "(alfa = 0,01) da diferença de perda quadrática. A versão 'pesos' (inverso do erro recente) é só reportada.",
)


def gerar(i):
    cen, k = SERIES[i]
    s = CEN[cen].gerar(k)
    season, season2 = s.get("season"), s.get("season2")

    def ref(dd):
        return Zero(dd) if cen in ("C01", "C04") else (SeasonalNaive(dd, season) if season else Naive(dd))

    def membros(dd):
        return [LebreW(dd, season=season, season2=season2), ref(dd)]

    s.update(grupo=cen, extras=[lambda dd: Porta(membros(dd), "m2_porta"),
                                lambda dd: PesosOnline(membros(dd), "m2_pesos")])
    return s


def _geo(v):
    v = np.asarray(v, float); v = v[np.isfinite(v) & (v > 0)]
    return float(np.exp(np.mean(np.log(v)))) if len(v) else float("nan")


def _ref(r):
    c = r["comparadores"]
    return c["zero"]["mse"] if "zero" in c else (c["sazonal_ingenuo"]["mse"] if "sazonal_ingenuo" in c else c["ingenuo"]["mse"])


def avaliar(resumo, series):
    tab = {}
    for g in NEGATIVOS + POSITIVOS:
        rs = [r for r in series if r["grupo"] == g]
        tab[g] = {k: dict(rel_referencia=_geo([r["extras"][k]["mse"] / _ref(r) for r in rs]),
                          rel_lebre=_geo([r["extras"][k]["mse_rel_lebre"] for r in rs])) for k in ("m2_porta", "m2_pesos")}
        tab[g]["lebre_rel_referencia"] = _geo([r["lebre"]["mse"] / _ref(r) for r in rs])
    resumo["por_familia"] = tab
    ok = all(tab[g]["m2_porta"]["rel_referencia"] <= 1.01 for g in NEGATIVOS) and \
        all(tab[g]["m2_porta"]["rel_lebre"] <= 1.02 for g in POSITIVOS)
    return "atende" if ok else "nao_atende"
