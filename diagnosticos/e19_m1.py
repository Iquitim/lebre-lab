"""E19 (plano: diagnosticos/E19_PLANO.md): M1 rascunho 4 (+ M2 Q2, como no E18b), só descrição; derivado de e17_m1.py. Para cada série: MSE (÷ v0.52) da
combinação L', do especialista recortado e do especialista sem recorte; peso s; fração de passos no recorte; excesso de L'
sobre a v0.52 por quinto do período de avaliação.

Uso: python -m diagnosticos.e19_m1"""
import json
from pathlib import Path

import numpy as np

from analises import m2_dev as M
from diagnosticos.e13_comum import KW, refnome, series

ALVOS = [("VB07", None), ("XB07", None), ("B07", None)]


def rastrear(s):
    y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
    T, d = X.shape
    kw = dict(KW, saida="prod_q2")
    m = M.Lebre053(d, season=s.get("season"), season2=s.get("season2"), referencia=refnome(s), precisao="r4", **kw)
    c = {k: np.full(T, np.nan) for k in ("L1", "L52", "e", "bruto", "s", "n")}
    for t in range(T):
        m.predict(X[t])
        p = m.precisao
        c["L1"][t] = m._L; c["L52"][t] = m._L52
        if p.e is not None:
            c["e"][t] = p.e; c["s"][t] = p.prod.s(); c["n"][t] = p.prod.n
            c["bruto"][t] = float(p.w @ p.z)
        m.observe(None if not np.isfinite(y[t]) else float(y[t]))
    return y, c


def main():
    out = []
    for fam, nome in ALVOS:
        for s in series(fam):
            if nome and s["nome"] != nome:
                continue
            y, c = rastrear(s)
            T = len(y)
            ini = int(0.2 * T)
            ok = np.zeros(T, bool); ok[ini:] = True
            ok &= np.isfinite(y) & np.isfinite(c["L52"])
            okE = ok & np.isfinite(c["e"])
            e52 = (c["L52"] - y) ** 2
            base = e52[ok].sum()
            exc = ((c["L1"] - y) ** 2 - e52)
            quintos = np.array_split(np.where(ok)[0], 5)
            r = dict(familia=fam, serie=s["nome"], T=T, n_aval=int(ok.sum()), passos_com_E=int(okE.sum()),
                     L1_sobre_52=float(((c["L1"] - y) ** 2)[ok].sum() / base),
                     E_recortado_sobre_52=float(((c["e"] - y) ** 2)[okE].sum() / e52[okE].sum()) if okE.any() else None,
                     E_bruto_sobre_52=float(((c["bruto"] - y) ** 2)[okE].sum() / e52[okE].sum()) if okE.any() else None,
                     frac_no_recorte=float(np.mean(np.abs(c["bruto"][okE] - c["e"][okE]) > 0)) if okE.any() else None,
                     s_medio=float(np.nanmean(c["s"][ok])) if okE.any() else None,
                     frac_sombra=float(np.mean(c["n"][okE] < 100)) if okE.any() else None,
                     reinicios_prod=int(np.sum(np.diff(c["n"][np.isfinite(c["n"])]) < 0)),
                     s_por_quinto=[round(float(np.nanmean(c["s"][q])), 3) for q in np.array_split(np.where(ok)[0], 5)],
                     excesso_por_quinto=[round(float(exc[q].sum() / base), 4) for q in quintos])
            out.append(r)
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
    Path(__file__).with_name("e19_m1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                                                       encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
