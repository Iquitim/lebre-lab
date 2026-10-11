"""Medição da validação 7 (regras e critérios: analises/VALIDACAO7_PLANO.md; congelamento: VALIDACAO7_CONGELADA.md).
Protótipo no commit cfe72ce. Por série: v0.54 com a M5a (base), com a M5b (m5b=True) e com a M4 (m4=True), cada uma
contra a base. Usa funções de m5a_e1, m5b_e1 e m4_e1 sem alteração.
Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit cfe72ce e LEBRE053_PROTO como antes):
  python -m analises.val7 FAM ...   |   python -m analises.val7 resumo
"""
import json
import math
import subprocess
import sys

import numpy as np

from analises import m2_dev as M
from analises import m4_e1 as M4
from analises import m5a_e1 as E
from analises import m5b_e1 as M5
from lab.run import ROOT, load

Lebre054 = E.Lebre054
OUT = E.AQUI / "val7"
COMMIT = "cfe72ce"
SEMENTE_BOOT = 2026101290
FAMILIAS = {"T-A01": "TA01_custo", "T-A05": "TA05_troca", "T-A07": "TA07_intermitente", "T-A02": "TA02_nulo",
            "T-B03": "TB03_qualidade_do_ar", "T-B06": "TB06_eolica"}
TROCA = 15000


def proto_info():
    commit = subprocess.run(["git", "-C", str(E.P54), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(["git", "-C", str(E.P54), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if commit != COMMIT or sujo.strip():
        raise SystemExit(f"validação 7 exige o protótipo limpo no commit {COMMIT} (encontrado {commit})")
    return dict(commit=commit)


def rodar(m, X, y):
    f = np.full(len(y), np.nan)
    for t in range(len(y)):
        yt = None if not math.isfinite(y[t]) else float(y[t])
        f[t] = m.step(X[t], yt).value
    return f


def familia(fid):
    info = proto_info()
    mod = load(ROOT / "scenarios" / "T" / f"{FAMILIAS[fid]}.py")
    L = 168 if fid.startswith("T-B") else 20
    series, reps = [], []
    for k, sd in enumerate(mod.SPEC["sementes"]):
        s = mod.gerar(sd)
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float)
        T, d = X.shape; ini = int(0.2 * T)
        kw = dict(season=s.get("season"), season2=s.get("season2"), reference=E.refnome(s))
        a, b5, b4 = Lebre054(d, **kw), Lebre054(d, m5b=True, **kw), Lebre054(d, m4=True, **kw)
        fa, f5, f4 = rodar(a, X, y), rodar(b5, X, y), rodar(b4, X, y)
        p, rep = M.par_bootstrap(y, f4, fa, ini, L, np.random.default_rng([SEMENTE_BOOT, list(FAMILIAS).index(fid), k]))
        reps.append(rep)
        ea, e4 = M4.eventos(a), M4.eventos(b4)
        series.append(dict(
            serie=s.get("nome"), T=T, d=d,
            m5b=dict(identica=bool(np.array_equal(fa, f5, equal_nan=True)), estrutura_igual=a.structure == b5.structure,
                     nucleo_sem=a.core.cost_per_step, nucleo_com=b5.core.cost_per_step,
                     triagem_sem=a.core._core.fp["screening"], equiv=M5.equivalentes(a, b5)),
            m4=dict(razao=p, nan_aval=int((np.isfinite(y) & ~np.isfinite(f4))[ini:].sum()),
                    identica=bool(np.array_equal(fa, f4, equal_nan=True)), sem_aceite=len(ea) == 0,
                    remocoes=[e for e in e4 if e["tipo"] == "rem"], estrutura_com=b4.structure,
                    custo_sem=a.cost_per_step, custo_com=b4.cost_per_step)))
        print(fid, s.get("nome"), "M5b idêntica", series[-1]["m5b"]["identica"], "M4 razão", round(p, 5),
              "remoções", series[-1]["m4"]["remocoes"], flush=True)
    rr = np.vstack(reps).mean(0); rr = rr[np.isfinite(rr)]
    logs = [math.log(x["m4"]["razao"]) for x in series if np.isfinite(x["m4"]["razao"]) and x["m4"]["razao"] > 0]
    resumo = dict(m4_geo=float(np.exp(np.mean(logs))), m4_ic95=[float(np.exp(np.quantile(rr, 0.025))),
                                                               float(np.exp(np.quantile(rr, 0.975)))], n=len(series))
    OUT.mkdir(exist_ok=True)
    (OUT / f"{fid}.json").write_text(json.dumps(dict(familia=fid, prototipo=info, semente=SEMENTE_BOOT, bloco=L,
                                                     resumo=resumo, series=series), indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
    print(fid, "resumo", resumo, flush=True)


def resumo():
    R = {f: json.loads((OUT / f"{f}.json").read_text(encoding="utf-8")) for f in FAMILIAS}
    S = [x for r in R.values() for x in r["series"]]
    # M5b
    c51 = all(x["m5b"]["identica"] and x["m5b"]["estrutura_igual"] for x in S)
    a50 = [x for x in R["T-A01"]["series"] if x["d"] == 50]
    r50 = float(np.mean([x["m5b"]["nucleo_com"] for x in a50]) / np.mean([x["m5b"]["nucleo_sem"] for x in a50]))
    c52 = all(x["m5b"]["nucleo_com"] <= x["m5b"]["nucleo_sem"] for x in S) and \
        all(x["m5b"]["nucleo_com"] < x["m5b"]["nucleo_sem"] for x in S if x["m5b"]["triagem_sem"] > 0) and r50 <= 0.80
    disc_fora = sum(x["m5b"]["equiv"]["disc_fora"] for x in S); pares = sum(x["m5b"]["equiv"]["pares_fora"] for x in S)
    disc_dentro = sum(x["m5b"]["equiv"]["disc_dentro"] for x in S)
    c53 = disc_fora == 0
    # M4
    rem_a05 = sum(any(e["sai"] == ["in", 0] and TROCA <= e["t"] <= TROCA + 10000 for e in x["m4"]["remocoes"])
                  for x in R["T-A05"]["series"])
    c41 = rem_a05 >= 14
    falsas_a01 = sum(any(e["sai"] in (["in", 0], ["in", 1]) for e in x["m4"]["remocoes"]) for x in R["T-A01"]["series"])
    falsas_a02 = sum(any(n.startswith("x") for n in x["m4"]["estrutura_com"]) for x in R["T-A02"]["series"])
    c42 = falsas_a01 == 0 and falsas_a02 == 0
    c43 = all(r["resumo"]["m4_ic95"][1] <= 1.02 for r in R.values()) and all(x["m4"]["nan_aval"] == 0 for x in S)
    c44 = all(x["m4"]["identica"] for x in S if x["m4"]["sem_aceite"])
    L = ["# Validação 7 (v0.54, M5b rascunho 1 e M4 rascunho 1): resultado", "",
         "Regras e critérios em `VALIDACAO7_PLANO.md`; congelamento em `VALIDACAO7_CONGELADA.md`. Protótipo no commit "
         f"`{COMMIT}`; cada mudança contra a v0.54 com a M5a. Usada uma única vez.", "",
         "| Família | séries | M5b: idênticas | núcleo sem → com | M4: razão de MSE | IC 95% | remoções |", "|---|---|---|---|---|---|---|"]
    for f, r in R.items():
        ss = r["series"]; z = r["resumo"]
        L.append(f"| {f} | {len(ss)} | {sum(x['m5b']['identica'] and x['m5b']['estrutura_igual'] for x in ss)} | "
                 f"{np.mean([x['m5b']['nucleo_sem'] for x in ss]):.0f} → {np.mean([x['m5b']['nucleo_com'] for x in ss]):.0f} | "
                 f"{z['m4_geo']:.4f} | {z['m4_ic95'][0]:.4f}–{z['m4_ic95'][1]:.4f} | {sum(len(x['m4']['remocoes']) for x in ss)} |")
    L += ["", "**M5b rascunho 1**", "",
          f"1. Identidade: {'atende' if c51 else 'não atende'}",
          f"2. Custo (nunca maior; menor onde a triagem roda; razão T-A01 d = 50: {r50:.3f}, limite 0,80): "
          f"{'atende' if c52 else 'não atende'}",
          f"3. Equivalentes (fora da faixa: {disc_fora} discordâncias em {pares} pares; dentro: {disc_dentro}, só reportado): "
          f"{'atende' if c53 else 'não atende'}", "",
          f"**Decisão pela regra do plano:** a M5b (rascunho 1) é **{'aceita' if c51 and c52 and c53 else 'não aceita'}**.", "",
          "**M4 rascunho 1**", "",
          f"1. T-A05 (x0 removida até 10.000 passos depois da troca, ≥ 14 de 20): {rem_a05} de 20 — {'atende' if c41 else 'não atende'}",
          f"2. Sem remoções falsas (T-A01: {falsas_a01}; T-A02: {falsas_a02}): {'atende' if c42 else 'não atende'}",
          f"3. Sem piora (limite superior ≤ 1,02 em todas; nenhuma previsão não finita): {'atende' if c43 else 'não atende'}",
          f"4. Identidade onde nenhuma unidade foi aceita: {'atende' if c44 else 'não atende'}", "",
          f"**Decisão pela regra do plano:** a M4 (rascunho 1) é **{'aceita' if c41 and c42 and c43 and c44 else 'não aceita'}**."]
    (E.AQUI / "VALIDACAO7_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("feito")


if __name__ == "__main__":
    if sys.argv[1] == "resumo":
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
