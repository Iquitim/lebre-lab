"""E13, parte B (plano: diagnosticos/E13_PLANO.md): a M1 em Y-B01. Só descrição."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from diagnosticos.e13_comum import rastrear, series


def main():
    out = []
    for s in series("YB01"):
        y, t1, m1 = rastrear(s, precisao="r2")
        _, t0, _ = rastrear(s, precisao=False)
        T = len(y); ini = int(0.2 * T)
        ok = np.zeros(T, bool); ok[ini:] = True
        ok &= np.isfinite(y) & np.isfinite(t1["out"]) & np.isfinite(t0["out"])
        e1, e0 = (t1["out"] - y) ** 2, (t0["out"] - y) ** 2
        base = e0[ok].sum(); exc = e1 - e0
        idx = pd.date_range(s["inicio"], periods=T, freq="h")
        df = pd.DataFrame({"exc": np.where(ok, exc, 0.0) / base}, index=idx)
        ativo = ok & (np.nan_to_num(t1["sE"]) > 0.5)
        yy = y[np.isfinite(y)]
        sel = m1.precisao.sel
        r = dict(serie=s["nome"], excesso=float(exc[ok].sum() / base),
                 excesso_s_maior_05=float(exc[ativo].sum() / base), passos_s_maior_05=int(ativo.sum()),
                 sE_medio=float(np.nanmean(t1["sE"][ok])), passos_no_corte=int(np.nansum(t1["corte"][ok])),
                 passos_com_E=int(np.isfinite(t1["e"][ok]).sum()),
                 por_mes={str(k.date())[:7]: round(float(v), 4) for k, v in df["exc"].resample("MS").sum().items()},
                 por_hora={int(k): round(float(v), 4) for k, v in df.groupby(df.index.hour)["exc"].sum().items()},
                 zeros=float((yy == 0).mean()), max=float(yy.max()),
                 corridas_constantes_24h=int(sum(1 for i in range(24, len(yy)) if np.ptp(yy[i - 24:i]) == 0 and yy[i - 1] > 0)),
                 selecionadas=[s["entradas"][j] for j in sel] if sel is not None else None)
        out.append(r)
        print({k: v for k, v in r.items() if k not in ("por_mes", "por_hora")}, flush=True)
    Path(__file__).with_name("e13_m1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                                                       encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
