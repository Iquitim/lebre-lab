"""Validação 4, critério 1 (plano: analises/M1_VAL4_PLANO.md; regra em VALIDACAO4_PLANO.md): F6 em Y-B03 pela fronteira.
Custo médio da v0.53 (M1 r2 + M2) <= 2,5 vezes o da v0.52 e erro (geo ÷ comparador linear online completo) <= 1,05 × o
menor erro entre as variantes do E10 recalculadas em Y-B03 (mesmas classes e fórmula de custo de diagnosticos/f6_e10.py,
com o d de Y-B03) com custo <= o da v0.53. Usada uma única vez. Derivado de m1_e12_alvo.py e f6_e10.py (inalterados).

Uso: python -m analises.m1_val4_alvo
"""
import json
import math

import numpy as np

from analises import m2_dev as M
from diagnosticos.f6_e10 import BANDAS, RLSBandas, fp
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics
from lab.run import ROOT, load

KW = dict(porta=True, eps_porta=0.002, recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod")


class Completo8(OnlineLinear):
    """Comparador completo atualizado a cada 8 alvos observados (como no E10)."""
    n = 0

    def observe(self, yy):
        v = math.nan if yy is None or not math.isfinite(yy) else yy
        if not math.isnan(v):
            self.n += 1
        if math.isnan(v) or self.n % 8:
            self.hist.append(v); return
        super().observe(yy)


def main():
    info = M.proto_info()
    mod = load(ROOT / "scenarios" / "Y" / "YB03_qualidade_do_ar.py")
    series, var = [], {}
    for i in mod.SPEC["sementes"]:
        s = mod.gerar(i)
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape; ini = int(0.2 * T)
        season, season2 = s.get("season"), s.get("season2")
        m1 = M.Lebre053(d, season=season, season2=season2, referencia="sazonal", precisao="r2", **KW)
        f1 = M.rodar(m1, X, y)
        m52 = M.Lebre053(d, season=season, season2=season2, porta=False)
        f52 = M.rodar(m52, X, y)
        comp = forecast_metrics(y, M.rodar_ref(OnlineLinear(d), X, y), ini)["mse"]
        ok = np.isfinite(y[:ini])
        r = np.array([abs(np.corrcoef(np.nan_to_num(X[:ini][ok, j]), y[:ini][ok])[0, 1]) for j in range(d)])
        top3 = np.argsort(-np.nan_to_num(r))[:3]
        linha = {}
        for nome, usa, bandas in (("AR2+0", np.arange(d), [(0, 0)]), ("AR2+B3", top3, BANDAS),
                                  ("AR2+B-todas", np.arange(d), BANDAS)):
            for cada in (1, 8):
                m = RLSBandas(usa, bandas, cada)
                linha[f"{nome}/{cada}"] = (forecast_metrics(y, M.rodar_ref(m, X, y), ini)["mse"] / comp,
                                           fp(m.k, len(usa), cada))
        k = 1 + 2 + d * 9
        linha["COMPLETO/1"] = (1.0, fp(k, 0, 1))
        linha["COMPLETO/8"] = (forecast_metrics(y, M.rodar_ref(Completo8(d), X, y), ini)["mse"] / comp, fp(k, 0, 8))
        for c, v in linha.items():
            var.setdefault(c, []).append(v)
        p1 = m1.precisao
        series.append(dict(serie=s["nome"], d=d, v053_sobre_linear=forecast_metrics(y, f1, ini)["mse"] / comp,
                           v052_sobre_linear=forecast_metrics(y, f52, ini)["mse"] / comp,
                           custo_v053=m1.cost_per_step, custo_v052=m52.cost_per_step,
                           selecionadas=[s["entradas"][j] for j in p1.sel] if p1.sel is not None else None,
                           peso_especialista_final=p1.prod.s(), variantes=linha))
        print(s["nome"], {k_: round(v, 4) for k_, v in series[-1].items() if isinstance(v, float)},
              {k_: round(v[0], 3) for k_, v in linha.items()}, flush=True)
    geo = lambda xs: float(np.exp(np.mean([math.log(x) for x in xs])))
    fronteira = {c: (geo([v[0] for v in vs]), float(np.mean([v[1] for v in vs]))) for c, vs in var.items()}
    custo = float(np.mean([x["custo_v053"] for x in series])); custo52 = float(np.mean([x["custo_v052"] for x in series]))
    obtido = geo([x["v053_sobre_linear"] for x in series])
    cabem = [e for e, c in fronteira.values() if c <= custo]
    melhor = min(cabem) if cabem else None
    ok1 = custo <= 2.5 * custo52 and melhor is not None and obtido <= 1.05 * melhor
    out = dict(prototipo=info, series=series, fronteira=fronteira,
               f6=dict(custo_v053=custo, custo_v052=custo52, razao_custo=custo / custo52, melhor_variante_no_custo=melhor,
                       meta=None if melhor is None else 1.05 * melhor, obtido=obtido,
                       v052_sobre_linear=geo([x["v052_sobre_linear"] for x in series])),
               criterio_1=ok1)
    (M.AQUI / "m1val4_alvo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                             newline="\n")
    L = ["# Validação 4, critério 1: F6 em Y-B03 (fronteira recalculada)", "",
         f"Protótipo `{info['commit']}`. Plano `M1_VAL4_PLANO.md`.", "",
         f"Custo da v0.53 em Y-B03 {custo:.0f} FP por passo ({custo / custo52:.2f} × v0.52, teto 2,5). Melhor variante com "
         f"custo <= esse: erro {'-' if melhor is None else f'{melhor:.3f}'}; meta "
         f"{'-' if melhor is None else f'{1.05 * melhor:.3f}'}; obtido {obtido:.3f} (v0.52: "
         f"{out['f6']['v052_sobre_linear']:.3f}).", "",
         f"**Critério 1: {'atendido' if ok1 else 'não atendido'}.**", "",
         "| Variante | erro (geo ÷ completo) | FP por passo |", "|---|---|---|"]
    L += [f"| {c} | {e:.3f} | {f:.0f} |" for c, (e, f) in fronteira.items()]
    L += ["", "| Série | v0.53 ÷ linear | v0.52 ÷ linear | custo v0.53 | custo v0.52 |", "|---|---|---|---|---|"]
    L += [f"| {x['serie']} | {x['v053_sobre_linear']:.3f} | {x['v052_sobre_linear']:.3f} | {x['custo_v053']:.0f} | "
          f"{x['custo_v052']:.0f} |" for x in series]
    (M.AQUI / "M1_VAL4_ALVO_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
