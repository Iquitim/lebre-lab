"""E18b, critério de F6 da M1 rascunho 4 com a M2 Q2 (plano: analises/E18B_PLANO.md; ALGORITHM_SPEC_DRAFT_M1_r4.md, seção 2);
derivado de m2_e16_alvo.py (inalterado). F6 nas famílias
em que a v0.52 está abaixo da fronteira (E14: B03, B07, VB07, XB07). Em cada uma: custo médio da v0.53 (M1 r4 + M2 Q2) <=
2,5 × o da v0.52 e erro (geo ÷ comparador linear online completo) <= 1,05 × o menor erro entre as 8 variantes do E14
(diagnosticos/e14/<família>.json, mesmas séries) com custo <= o da v0.53. Sem sorteio.

Uso: python -m analises.m2_e18b_alvo
"""
import json
import math
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from diagnosticos.e13_comum import series
from lab.baselines import OnlineLinear
from lab.metrics import forecast_metrics

FAMILIAS = ["B03", "B07", "VB07", "XB07"]
E14 = Path(__file__).resolve().parents[1] / "diagnosticos" / "e14"
KW = dict(porta=True, eps_porta=0.002, recriar=True, alpha_porta=0.01, observar_quarentena_entradas=True, saida="prod_q2")


def _ref(s):
    return "zero" if s.get("zero_baseline") else ("sazonal" if s.get("season") else "persistencia")


def main():
    info = M.proto_info()
    out = dict(prototipo=info, familias={})
    L = ["# E18b: F6 nas famílias abaixo da fronteira (M1 rascunho 4 + M2 Q2)", "", f"Protótipo `{info['commit']}`. "
         "Plano `E18B_PLANO.md`.", "",
         "| Família | custo v0.53 ÷ v0.52 | erro v0.53 | erro v0.52 | e* no custo da v0.53 (variante) | meta | atende |",
         "|---|---|---|---|---|---|---|"]
    tudo = True
    for fam in FAMILIAS:
        var = {x["serie"]: x["v"] for x in json.loads((E14 / f"{fam}.json").read_text(encoding="utf-8"))}
        linhas = []
        for s in series(fam):
            y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
            T, d = X.shape
            ini = int(0.2 * T)
            m = M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), referencia=_ref(s), precisao="r4", **KW)
            f = M.rodar(m, X, y)
            m52 = M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), porta=False)
            f52 = M.rodar(m52, X, y)
            comp = forecast_metrics(y, M.rodar_ref(OnlineLinear(d), X, y), ini)["mse"]
            linhas.append(dict(serie=s["nome"], erro=forecast_metrics(y, f, ini)["mse"] / comp,
                               erro_v052=forecast_metrics(y, f52, ini)["mse"] / comp, custo=m.cost_per_step,
                               custo_v052=m52.cost_per_step, peso_especialista=m.precisao.prod.s(),
                               variantes=var[s["nome"]]))
            print(fam, s["nome"], round(linhas[-1]["erro"], 3), round(linhas[-1]["erro_v052"], 3),
                  round(linhas[-1]["custo"]), flush=True)
        geo = lambda xs: float(np.exp(np.mean([math.log(x) for x in xs])))
        nomes = [n for n in linhas[0]["variantes"] if n != "v0.52"]
        fr = {n: (geo([x["variantes"][n][0] for x in linhas]), float(np.mean([x["variantes"][n][1] for x in linhas])))
              for n in nomes}
        c = float(np.mean([x["custo"] for x in linhas]))
        c52 = float(np.mean([x["custo_v052"] for x in linhas]))
        cand = [(e, n) for n, (e, cc) in fr.items() if cc <= c]
        estrela, nome = min(cand) if cand else (math.nan, "-")
        erro, erro52 = geo([x["erro"] for x in linhas]), geo([x["erro_v052"] for x in linhas])
        ok = c <= 2.5 * c52 and erro <= 1.05 * estrela
        tudo &= ok
        out["familias"][fam] = dict(series=linhas, fronteira=fr, custo=c, custo_v052=c52, e_estrela=estrela,
                                    variante=nome, erro=erro, erro_v052=erro52, atende=ok)
        L.append(f"| {fam} | {c / c52:.2f} | {erro:.3f} | {erro52:.3f} | {estrela:.3f} ({nome}) | {1.05 * estrela:.3f} | "
                 f"{'sim' if ok else '**não**'} |")
    out["criterio_1"] = tudo
    L += ["", f"**Critério 1 (F6 nas famílias abaixo da fronteira): {'atendido' if tudo else 'não atendido'}.**"]
    (M.AQUI / "e18b_alvo.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                         newline="\n")
    (M.AQUI / "E18B_ALVO_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
