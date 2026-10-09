"""Validação 5, critério 1 (plano: analises/M1_VAL5_PLANO.md; regra em VALIDACAO5_PLANO.md): F6 em Z-B03 e Z-B07 pela
fronteira. Por família: custo médio da v0.53 (M1 r5 + M2 Q2) <= 2,5 vezes o da v0.52 e erro (geo ÷ comparador linear
online completo) <= 1,05 × o menor erro entre as 8 variantes do E14 recalculadas na família (mesmas classes e fórmula de
custo de diagnosticos/f6_e10.py, com o d da família) com custo <= o da v0.53. Sem sorteio. Usada uma única vez.
Derivado de m1_val4_alvo.py e m2_e16_alvo.py (inalterados).

Uso: python -m analises.m1_val5_alvo
"""
import json
import math

import numpy as np

from analises import m2_dev as M
from analises.m1_val4_alvo import Completo8
from diagnosticos.f6_e10 import BANDAS, RLSBandas, fp
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

FAMILIAS = {"ZB03": "Z/ZB03_qualidade_do_ar.py", "ZB07": "Z/ZB07_mare.py"}
KW = dict(porta=True, eps_porta=0.002, recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod_q2",
          precisao="r5")


def _ref(s):
    return "zero" if s.get("zero_baseline") else ("sazonal" if s.get("season") else "persistencia")


def _geo(xs):
    return float(np.exp(np.mean([math.log(x) for x in xs])))


def main():
    info = M.proto_info()
    out = dict(prototipo=info, familias={})
    L = ["# Validação 5, critério 1: F6 em Z-B03 e Z-B07 (fronteira recalculada)", "",
         f"Protótipo `{info['commit']}`. Plano `M1_VAL5_PLANO.md`.", "",
         "| Família | custo v0.53 ÷ v0.52 | erro v0.53 | erro v0.52 | e* no custo da v0.53 (variante) | meta | atende |",
         "|---|---|---|---|---|---|---|"]
    tudo = True
    for fam, arq in FAMILIAS.items():
        mod = load(ROOT / "scenarios" / arq)
        series = []
        for i in mod.SPEC["sementes"]:
            s = mod.gerar(i)
            y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
            T, d = X.shape
            ini = int(0.2 * T)
            season, season2 = s.get("season"), s.get("season2")
            m = M.Lebre053(d, season=season, season2=season2, referencia=_ref(s), **KW)
            f = M.rodar(m, X, y)
            m52 = M.Lebre053(d, season=season, season2=season2, porta=False)
            f52 = M.rodar(m52, X, y)
            comp = forecast_metrics(y, M.rodar_ref(OnlineLinear(d), X, y), ini)["mse"]
            ok = np.isfinite(y[:ini])
            r = np.array([abs(np.corrcoef(np.nan_to_num(X[:ini][ok, j]), y[:ini][ok])[0, 1]) for j in range(d)])
            top3 = np.argsort(-np.nan_to_num(r))[:3]
            var = {}
            for nome, usa, bandas in (("AR2+0", np.arange(d), [(0, 0)]), ("AR2+B3", top3, BANDAS),
                                      ("AR2+B-todas", np.arange(d), BANDAS)):
                for cada in (1, 8):
                    rm = RLSBandas(usa, bandas, cada)
                    var[f"{nome}/{cada}"] = (forecast_metrics(y, M.rodar_ref(rm, X, y), ini)["mse"] / comp,
                                             fp(rm.k, len(usa), cada))
            k = 3 + 9 * d
            var["COMPLETO/1"] = (1.0, fp(k, 0, 1))
            var["COMPLETO/8"] = (forecast_metrics(y, M.rodar_ref(Completo8(d), X, y), ini)["mse"] / comp, fp(k, 0, 8))
            nan = int((np.isfinite(y) & ~np.isfinite(f))[ini:].sum())
            series.append(dict(serie=s["nome"], d=d, erro=forecast_metrics(y, f, ini)["mse"] / comp,
                               erro_v052=forecast_metrics(y, f52, ini)["mse"] / comp, custo=m.cost_per_step,
                               custo_v052=m52.cost_per_step, peso_especialista=m.precisao.peso(), nan_aval=nan,
                               variantes=var))
            print(fam, s["nome"], round(series[-1]["erro"], 3), round(series[-1]["erro_v052"], 3), round(m.cost_per_step),
                  flush=True)
        nomes = list(series[0]["variantes"])
        fr = {n: (_geo([x["variantes"][n][0] for x in series]), float(np.mean([x["variantes"][n][1] for x in series])))
              for n in nomes}
        c = float(np.mean([x["custo"] for x in series]))
        c52 = float(np.mean([x["custo_v052"] for x in series]))
        cand = [(e, n) for n, (e, cc) in fr.items() if cc <= c]
        estrela, nome = min(cand) if cand else (math.nan, "-")
        erro, erro52 = _geo([x["erro"] for x in series]), _geo([x["erro_v052"] for x in series])
        nan = sum(x["nan_aval"] for x in series)
        ok = c <= 2.5 * c52 and erro <= 1.05 * estrela and nan == 0
        tudo &= ok
        out["familias"][fam] = dict(series=series, fronteira=fr, custo=c, custo_v052=c52, e_estrela=estrela, variante=nome,
                                    erro=erro, erro_v052=erro52, nan_aval=nan, atende=ok)
        L.append(f"| {fam} | {c / c52:.2f} | {erro:.3f} | {erro52:.3f} | {estrela:.3f} ({nome}) | {1.05 * estrela:.3f} | "
                 f"{'sim' if ok else '**não**'} |")
    out["criterio_1"] = tudo
    L += ["", f"**Critério 1 (F6): {'atendido' if tudo else 'não atendido'}.**", ""]
    for fam, v in out["familias"].items():
        L += [f"Fronteira em {fam}:", "", "| Variante | erro | FP |", "|---|---|---|"]
        L += [f"| {n} | {e:.3f} | {cc:.0f} |" for n, (e, cc) in v["fronteira"].items()]
        L.append("")
    (M.AQUI / "m1val5_alvo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                             newline="\n")
    (M.AQUI / "M1_VAL5_ALVO_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
