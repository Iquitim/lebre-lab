"""E13, parte A (plano: diagnosticos/E13_PLANO.md): de onde vem o excesso da M2 (P) sobre a referência. Só descrição."""
import json
from pathlib import Path

import numpy as np

from diagnosticos.e13_comum import rastrear, series

ALVOS = [("YC01", None), ("YB07", "8418150_Portland"), ("C01", None), ("XC01", None)]


def main():
    out = []
    for fam, so in ALVOS:
        for s in series(fam):
            if so and s["nome"] != so:
                continue
            y, tr, _ = rastrear(s)
            T = len(y); ini = int(0.2 * T)
            ok = np.zeros(T, bool); ok[ini:] = True
            ok &= np.isfinite(y) & np.isfinite(tr["R"]) & np.isfinite(tr["out"])
            okD = ok & np.isfinite(tr["D"])
            eR, eP = (tr["R"] - y) ** 2, (tr["out"] - y) ** 2
            eD = np.where(okD, (tr["D"] - y) ** 2, eP)                  # sem D definido, P = L e conta como parcela de D
            base = eR[ok].sum()
            exc = eP - eR
            top = ok & (eR >= np.quantile(eR[ok], 0.99))
            meio = ini + (T - ini) // 2
            r = dict(familia=fam, serie=s["nome"], n=int(ok.sum()),
                     excesso=float(exc[ok].sum() / base),
                     parcela_prod=float((eP - eD)[ok].sum() / base), parcela_D=float((eD - eR)[ok].sum() / base),
                     excesso_top1pct=float(exc[top].sum() / base), excesso_1o_meio=float(exc[ok & (np.arange(T) < meio)].sum() / base),
                     excesso_2o_meio=float(exc[ok & (np.arange(T) >= meio)].sum() / base),
                     s_medio=float(np.nanmean(tr["s"][ok])), wD_L=float(np.nanmean(tr["wD_L"][ok])),
                     wM_L=float(np.nanmean(tr["wM_L"][ok])), L_sobre_R=float(((tr["L"] - y) ** 2)[ok].sum() / base))
            # os 5 passos de maior excesso: data e tamanho
            idx = np.argsort(-np.where(ok, exc, -np.inf))[:5]
            datas = s.get("datas")
            r["maiores"] = [dict(t=int(t), excesso=float(exc[t] / base), y=float(y[t]), R=float(tr["R"][t]),
                                 L=float(tr["L"][t]), wD_L=float(tr["wD_L"][t])) for t in idx]
            out.append(r)
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "maiores"}, flush=True)
    Path(__file__).with_name("e13_m2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                                                       encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
