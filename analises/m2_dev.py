"""Medição da M2 (v0.53) no banco de desenvolvimento. Plano: analises/M2_DEV_PLANO.md (commitado antes de rodar).

Uso (LEBRE053_PROTO = pasta experiments/LEBRE-V0.53-PROTO-01 do lebre-research):
    python -m analises.m2_dev A01 B02 ...     grava analises/m2dev/<FAM>.json
    python -m analises.m2_dev --resumo        aplica critérios e regra de escolha; grava analises/M2_DEV_RESULTADO.md
"""
import csv
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from lab.baselines import Naive, SeasonalNaive, Zero
from lab.metrics import forecast_metrics, structure_metrics
from lab.run import ROOT, load

PROTO = Path(os.environ["LEBRE053_PROTO"]).resolve()
sys.path.insert(0, str(PROTO))
from lebre053 import Lebre053  # noqa: E402

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "m2dev"
B, SEMENTE = 2000, 20261008
CONFIGS = {"R0": (0.0, True), "R2": (0.002, True), "R5": (0.005, True),
           "P0": (0.0, False), "P2": (0.002, False), "P5": (0.005, False)}
NEG = ["C01", "C03", "C04"]
POS = [f"A{i:02d}" for i in range(1, 13)] + ["B01", "B02", "B03", "B06", "B07", "C02", "C05"]
NULOS = ["A02", "C01", "C04"]
ARQ = {"A01": "A/A01_muitas_entradas.py", "A02": "A/A02_nulo.py", "A03": "A/A03_substitutas.py",
       "A04": "A/A04_atrasos_longos.py", "A05": "A/A05_mudanca_regime.py", "A06": "A/A06_deriva.py",
       "A07": "A/A07_intermitente.py", "A08": "A/A08_faltantes.py", "A09": "A/A09_outliers_sensor_travado.py",
       "A10": "A/A10_nao_linear.py", "A11": "A/A11_caudas_pesadas.py", "A12": "A/A12_escala.py",
       "B01": "B/B01_solar.py", "B02": "B/B02_carga_eletrica.py", "B03": "B/B03_qualidade_do_ar.py",
       "B06": "B/B06_eolica.py", "B07": "B/B07_mare_meteorologica.py", "C01": "C/C01_retornos.py",
       "C02": "C/C02_volatilidade.py", "C03": "C/C03_niveis_de_preco.py", "C04": "C/C04_juros.py",
       "C05": "C/C05_macro_mensal_curta.py"}
ORDEM = list(ARQ)


def bloco(fam):
    return 168 if fam.startswith("B") else (12 if fam == "C05" else 20)


def proto_info():
    sujo = subprocess.run(["git", "-C", str(PROTO), "status", "--porcelain", "--", "."], capture_output=True, text=True).stdout
    if sujo.strip():
        raise SystemExit(f"protótipo com alterações não commitadas:\n{sujo}")
    commit = subprocess.run(["git", "-C", str(PROTO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    return dict(commit=commit, model053_sha256=hashlib.sha256((PROTO / "lebre053" / "model053.py").read_bytes()).hexdigest())


def registro_lebre_mse(cen_id):
    """MSE da v0.52 por série na execução registrada mais recente do cenário."""
    rows = [r for r in csv.DictReader(open(ROOT / "runs" / "REGISTRO.csv", encoding="utf-8"))
            if r["cenario"] == cen_id and r["resultado"] != "abortado"]
    det = json.loads((ROOT / "runs" / rows[-1]["id"] / "detalhes.json").read_text(encoding="utf-8"))
    return rows[-1]["id"], {s["nome"]: s["lebre"]["mse"] for s in det["series"]}


def rodar(m, X, y):
    T = len(y); f = np.full(T, np.nan)
    for t in range(T):
        f[t] = m.step(X[t], None if not math.isfinite(y[t]) else float(y[t])).value
    return f


def rodar_ref(r, X, y):
    T = len(y); f = np.full(T, np.nan)
    for t in range(T):
        f[t] = r.predict(X[t]); r.observe(None if not math.isfinite(y[t]) else float(y[t]))
    return f


def externas(events):
    return sum(1 for e in events if e.outcome == "accepted" and e.added and e.added.startswith("x"))


def par_bootstrap(y, a, b, ini, L, rng):
    ok = np.isfinite(y) & np.isfinite(a) & np.isfinite(b); ok[:ini] = False
    la, lb = np.where(ok, (y - a) ** 2, 0.0), np.where(ok, (y - b) ** 2, 0.0)
    ponto = la[ok].sum() / lb[ok].sum()
    ca, cb = np.r_[0, np.cumsum(la[ini:])], np.r_[0, np.cumsum(lb[ini:])]
    n = len(la) - ini; m = n // L
    st = rng.integers(0, n - L + 1, size=(B, m))
    with np.errstate(divide="ignore", invalid="ignore"):
        rep = np.log((ca[st + L] - ca[st]).sum(1) / (cb[st + L] - cb[st]).sum(1))
    return float(ponto), rep


def familia(fam):
    info = proto_info()
    mod = load(ROOT / "scenarios" / ARQ[fam])
    run_id, reg = registro_lebre_mse(mod.SPEC["id"])
    series = []
    reps = {c: {"vs_ref": [], "vs_v052": []} for c in CONFIGS}
    for i in mod.SPEC["sementes"]:
        s = mod.gerar(i)
        y, X = np.asarray(s["y"], float), np.asarray(s["X"], float); T, d = X.shape
        season, season2, zero = s.get("season"), s.get("season2"), s.get("zero_baseline")
        refnome = "zero" if zero else ("sazonal" if season else "persistencia")
        ref = Zero(d) if zero else (SeasonalNaive(d, season) if season else Naive(d))
        ini = int(0.2 * T)
        m52 = Lebre053(d, season=season, season2=season2, porta=False); f52 = rodar(m52, X, y)
        fr = rodar_ref(ref, X, y)
        mse52 = forecast_metrics(y, f52, ini)["mse"]
        reg_mse = reg.get(s["nome"])
        linha = dict(serie=s["nome"], T=T, referencia=refnome, mse_v052=mse52, mse_ref=forecast_metrics(y, fr, ini)["mse"],
                     reproducao_dif_rel=None if reg_mse is None else abs(mse52 - reg_mse) / reg_mse,
                     externas_v052=externas(m52.events), custo_v052=m52.cost_per_step, configs={})
        if s.get("truth") is not None:
            linha["recall_v052"] = structure_metrics(m52.events, m52.structure, s["truth"])["recall"]
        rng = np.random.default_rng([SEMENTE, ORDEM.index(fam), i])
        for c, (eps, recriar) in CONFIGS.items():
            m = Lebre053(d, season=season, season2=season2, referencia=refnome, porta=True, eps_porta=eps, recriar=recriar)
            f = rodar(m, X, y)
            portas = [e for e in m.events if e.change == "gate"]
            r = dict(mse=forecast_metrics(y, f, ini)["mse"], trocas=m.trocas, trocas_por_2000=m.trocas / T * 2000,
                     primeira_promocao=next((e.t for e in portas if e.added == "lebre"), None),
                     externas=externas(m.events), custo=m.cost_per_step, acrescimo_custo=m.cost_per_step - m52.cost_per_step,
                     cobertura=m.coverage)
            if s.get("truth") is not None:
                r["recall"] = structure_metrics(m.events, m.structure, s["truth"])["recall"]
            p1, rep1 = par_bootstrap(y, f, fr, ini, bloco(fam), rng)
            p2, rep2 = par_bootstrap(y, f, f52, ini, bloco(fam), rng)
            r.update(razao_ref=p1, razao_v052=p2)
            reps[c]["vs_ref"].append(rep1); reps[c]["vs_v052"].append(rep2)
            linha["configs"][c] = r
        series.append(linha)
    resumo = {}
    for c in CONFIGS:
        out = {}
        for k, chave in (("vs_ref", "razao_ref"), ("vs_v052", "razao_v052")):
            logs = np.array([math.log(s_["configs"][c][chave]) for s_ in series])
            rr = np.vstack(reps[c][k]).mean(0); rr = rr[np.isfinite(rr)]
            out[k] = dict(geo=float(np.exp(logs.mean())), ic95=[float(np.exp(np.quantile(rr, 0.025))),
                                                                 float(np.exp(np.quantile(rr, 0.975)))])
        out["trocas_por_2000"] = float(np.mean([s_["configs"][c]["trocas_por_2000"] for s_ in series]))
        out["series_com_externa"] = int(sum(s_["configs"][c]["externas"] > 0 for s_ in series))
        out["acrescimo_custo"] = float(np.mean([s_["configs"][c]["acrescimo_custo"] for s_ in series]))
        resumo[c] = out
    res = dict(familia=fam, prototipo=info, execucao_lab_conferida=run_id, B=B, semente=SEMENTE, bloco=bloco(fam),
               series_com_externa_v052=int(sum(s_["externas_v052"] > 0 for s_ in series)),
               max_dif_reproducao=max((s_["reproducao_dif_rel"] or 0.0) for s_ in series),
               resumo=resumo, series=series)
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / f"{fam}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(fam, "reprodução v0.52:", res["max_dif_reproducao"], "| R2 vs_ref", round(resumo["R2"]["vs_ref"]["geo"], 4),
          "vs_v052", round(resumo["R2"]["vs_v052"]["geo"], 4), flush=True)


def resumo_geral():
    D = {f: json.loads((SAIDA / f"{f}.json").read_text(encoding="utf-8")) for f in ORDEM}
    L = ["# Medição da M2 (v0.53) no banco de desenvolvimento: resultado", "",
         f"Plano: `M2_DEV_PLANO.md`. Protótipo: commit `{D['A01']['prototipo']['commit']}`. Bootstrap de blocos pareado, "
         f"B = {B}, semente {SEMENTE}.", "",
         "Reprodução da v0.52 (MSE contra o registro do Lab): maior diferença relativa "
         f"{max(d['max_dif_reproducao'] for d in D.values()):.1e}.", ""]
    escolha = {}
    for c in CONFIGS:
        crit = {}
        crit[1] = all(D[f]["resumo"][c]["vs_ref"]["ic95"][1] <= 1.01 for f in NEG)
        crit[2] = all(D[f]["resumo"][c]["vs_v052"]["ic95"][1] <= 1.02 for f in POS)
        crit[3] = all(D[f]["resumo"][c]["trocas_por_2000"] <= 1 for f in ORDEM)
        crit[4] = all(D[f]["resumo"][c]["series_com_externa"] <= D[f]["series_com_externa_v052"] for f in NULOS)
        crit[5] = all(D[f]["resumo"][c]["acrescimo_custo"] <= 25 for f in ORDEM)
        neg = float(np.exp(np.mean([math.log(D[f]["resumo"][c]["vs_ref"]["geo"]) for f in NEG])))
        escolha[c] = (crit, neg)
    L += ["## Critérios por configuração", "", "| Config | ε | Hipóteses | 1 negativas | 2 positivas | 3 alternância | 4 falsas | 5 custo | M2 ÷ ref nas negativas (geo) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for c, (eps, rec) in CONFIGS.items():
        crit, neg = escolha[c]
        L.append(f"| {c} | {eps} | {'recriadas' if rec else 'persistentes'} | " + " | ".join("sim" if crit[k] else "**não**" for k in range(1, 6))
                 + f" | {neg:.4f} |")
    aptas = [c for c in CONFIGS if all(escolha[c][0].values())]
    if aptas:
        aptas.sort(key=lambda c: (round(escolha[c][1], 3), CONFIGS[c][0], not CONFIGS[c][1]))
        L += ["", f"**Escolha (regra da seção 4 do plano): {aptas[0]}.** Configurações aptas: {', '.join(aptas)}."]
    else:
        L += ["", "**Nenhuma configuração atende aos 5 critérios. Nenhuma é escolhida** (seção 4 do plano)."]
    L += ["", "## Detalhe por família (todas as configurações)", "",
          "| Família | Config | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | trocas/2000 | séries c/ externa (v0.52) | +custo |",
          "|---|---|---|---|---|---|---|"]
    for f in ORDEM:
        for c in CONFIGS:
            r = D[f]["resumo"][c]
            L.append(f"| {f} | {c} | {r['vs_ref']['geo']:.3f} ({r['vs_ref']['ic95'][0]:.3f}–{r['vs_ref']['ic95'][1]:.3f}) | "
                     f"{r['vs_v052']['geo']:.3f} ({r['vs_v052']['ic95'][0]:.3f}–{r['vs_v052']['ic95'][1]:.3f}) | "
                     f"{r['trocas_por_2000']:.2f} | {r['series_com_externa']} ({D[f]['series_com_externa_v052']}) | {r['acrescimo_custo']:.1f} |")
    (AQUI / "M2_DEV_RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L[:25]))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo_geral()
    else:
        for f in sys.argv[1:]:
            familia(f)
