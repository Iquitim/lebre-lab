"""Incerteza dos resultados centrais (plano em analises/INCERTEZA_PLANO.md, commitado antes de calcular).

Uso: python -m analises.incerteza B01 B02 ...   grava analises/incerteza_<FAM>.json para cada família
     python -m analises.incerteza --resumo      junta os arquivos em analises/INCERTEZA_RESULTADO.md
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

import lebre
from lab.baselines import Naive, SeasonalNaive, Zero
from lab.ensembles import LebreW, Porta
from lab.run import ROOT, load, run_series

AQUI = Path(__file__).resolve().parent
B, SEMENTE = 2000, 20261007
ARQ = {"B01": "B/B01_solar.py", "B02": "B/B02_carga_eletrica.py", "B03": "B/B03_qualidade_do_ar.py",
       "B06": "B/B06_eolica.py", "B07": "B/B07_mare_meteorologica.py", "C01": "C/C01_retornos.py",
       "C02": "C/C02_volatilidade.py", "C03": "C/C03_niveis_de_preco.py", "C04": "C/C04_juros.py",
       "C05": "C/C05_macro_mensal_curta.py"}
ORDEM = list(ARQ)
BLOCO = {**{f: 168 for f in ("B01", "B02", "B03", "B06", "B07")}, **{f: 20 for f in ("C01", "C02", "C03", "C04")}, "C05": 12}
REF = {"B01": "sazonal_ingenuo", "B02": "sazonal_ingenuo", "B03": "sazonal_ingenuo", "B06": "sazonal_ingenuo",
       "B07": "ingenuo", "C01": "zero", "C02": "ingenuo", "C03": "ingenuo", "C04": "zero", "C05": "ingenuo"}
# execuções originais cujos números precisam ser reproduzidos
ORIGINAL = {"B01": "20261004-183239_B01", "B02": "20261004-183302_B02", "B03": "20261004-183309_B03",
            "B06": "20261004-183324_B06", "B07": "20261004-183352_B07", "C01": "20261004-184211_C01",
            "C02": "20261004-184213_C02", "C03": "20261004-184216_C03", "C04": "20261004-184218_C04",
            "C05": "20261004-184218_C05"}
PORTA_ORIGINAL = {**{f: "20261006-063405_D04" for f in ("C01", "C03", "C04", "B01", "B02")},
                  **{f: "20261006-064338_D05c" for f in ("B03", "B06", "B07", "C02", "C05")}}


class SemEntradas:
    """LEBRE sem entradas externas (uma entrada constante zero), como no diagnóstico F9."""
    name = "sem_entradas"

    def __init__(self, season=None, season2=None):
        self.m = lebre.Lebre(1, season=season, season2=season2)

    def predict(self, x):
        return self.m.predict([0.0]).value

    def observe(self, y):
        self.m.observe(y)


def _detalhes(run_id):
    return json.loads((ROOT / "runs" / run_id / "detalhes.json").read_text(encoding="utf-8"))


def _par_bootstrap(y, a, b, ini, L, rng):
    """Razão de MSE a ÷ b no ponto e B réplicas de log-razão por bootstrap de blocos móveis (pareado)."""
    ok = np.isfinite(y) & np.isfinite(a) & np.isfinite(b)
    ok[:ini] = False
    la, lb = np.where(ok, (y - a) ** 2, 0.0), np.where(ok, (y - b) ** 2, 0.0)
    ponto = la[ok].sum() / lb[ok].sum()
    ca, cb = np.r_[0, np.cumsum(la[ini:])], np.r_[0, np.cumsum(lb[ini:])]
    n = len(la) - ini; m = n // L
    st = rng.integers(0, n - L + 1, size=(B, m))
    sa = (ca[st + L] - ca[st]).sum(1); sb = (cb[st + L] - cb[st]).sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        rep = np.log(sa / sb)
    return float(ponto), rep


def familia(fam):
    mod = load(ROOT / "scenarios" / ARQ[fam])
    det = {r["nome"]: r for r in _detalhes(ORIGINAL[fam])["series"]}
    detp = {r["nome"]: r for r in _detalhes(PORTA_ORIGINAL[fam])["series"] if r["grupo"] == fam}
    comps = {}
    conferencia = []
    for i in mod.SPEC["sementes"]:
        s = mod.gerar(i)
        season, season2, zero = s.get("season"), s.get("season2"), s.get("zero_baseline")

        def ref_m2(dd, season=season, zero=zero):
            return Zero(dd) if zero else (SeasonalNaive(dd, season) if season else Naive(dd))

        s["extras"] = [lambda dd, season=season, season2=season2, r=ref_m2: Porta([LebreW(dd, season=season, season2=season2),
                                                                                   r(dd)], "m2_porta")]
        if fam == "C03":
            s["extras"].append(lambda dd: SemEntradas())
        s["guardar_previsoes"] = True
        r = run_series(s, 0.2)
        p = r["_previsoes"]; px = r["_extras_previsoes"]
        # conferência de reprodutibilidade
        o = det[r["nome"]]; op = detp[r["nome"]]
        chk = {"lebre": (r["lebre"]["mse"], o["lebre"]["mse"]),
               **{k: (r["comparadores"][k]["mse"], o["comparadores"][k]["mse"]) for k in o["comparadores"]},
               "m2_porta": (r["extras"]["m2_porta"]["mse"], op["extras"]["m2_porta"]["mse"])}
        difs = {k: abs(a - b) / abs(b) for k, (a, b) in chk.items()}
        conferencia.append(dict(serie=r["nome"], max_dif_relativa=max(difs.values()), por_modelo=difs))
        rng = np.random.default_rng([SEMENTE, ORDEM.index(fam), i])
        y, ini, L = p["y"], p["inicio"], BLOCO[fam]
        pares = {"lebre/linear_online": (p["lebre"], p["linear_online"]),
                 f"lebre/{REF[fam]}": (p["lebre"], p[REF[fam]])}
        if fam in ("C01", "C03", "C04"):
            refm2 = "zero" if zero else ("sazonal_ingenuo" if season else "ingenuo")
            pares[f"porta/{refm2}"] = (px["m2_porta"], p[refm2])
        else:
            pares["porta/lebre"] = (px["m2_porta"], p["lebre"])
        if fam == "C03":
            pares["lebre/sem_entradas"] = (p["lebre"], px["sem_entradas"])
        for nome, (a, b) in pares.items():
            ponto, rep = _par_bootstrap(y, a, b, ini, L, rng)
            comps.setdefault(nome, []).append(dict(serie=r["nome"], razao=ponto, rep=rep))
    out = dict(familia=fam, bloco=BLOCO[fam], B=B, semente=SEMENTE, conferencia=conferencia, comparacoes={})
    for nome, lst in comps.items():
        logs = np.array([math.log(x["razao"]) for x in lst])
        reps = np.vstack([x["rep"] for x in lst]).mean(0)
        reps = reps[np.isfinite(reps)]
        out["comparacoes"][nome] = dict(n_series=len(lst), razao_geo=float(np.exp(logs.mean())),
                                        ic95=[float(np.exp(np.quantile(reps, 0.025))), float(np.exp(np.quantile(reps, 0.975)))],
                                        series_abaixo_de_1=int((logs < 0).sum()),
                                        por_serie={x["serie"]: round(x["razao"], 4) for x in lst})
    (AQUI / f"incerteza_{fam}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                                newline="\n")
    print(fam, "max diferença relativa na reprodução:", max(c["max_dif_relativa"] for c in conferencia))


def leitura(nome, ic):
    lo, hi = ic
    if nome.startswith("porta/lebre"):
        return "confirmado (<= 1,02)" if hi <= 1.02 else "não confirmado"
    return "consistente: melhor" if hi < 1 else ("consistente: pior" if lo > 1 else "inconclusivo")


def resumo():
    linhas = ["# Incerteza dos resultados centrais: resultado", "",
              "Plano: `INCERTEZA_PLANO.md` (commitado antes do cálculo). Bootstrap de blocos móveis pareado dentro de cada "
              f"série, B = {B}, semente {SEMENTE}; intervalo de 95% por percentis da média geométrica da família.", "",
              "## Reprodutibilidade", "", "| Família | Maior diferença relativa de MSE contra as execuções originais |",
              "|---|---|"]
    dados = {f: json.loads((AQUI / f"incerteza_{f}.json").read_text(encoding="utf-8")) for f in ORDEM
             if (AQUI / f"incerteza_{f}.json").exists()}
    for f, d in dados.items():
        linhas.append(f"| {f} | {max(c['max_dif_relativa'] for c in d['conferencia']):.1e} |")
    linhas += ["", "## Comparações", "", "| Família | Comparação | Séries | Razão (média geom.) | IC 95% | Séries < 1 | Leitura |",
               "|---|---|---|---|---|---|---|"]
    for f, d in dados.items():
        for nome, c in d["comparacoes"].items():
            linhas.append(f"| {f} | {nome} | {c['n_series']} | {c['razao_geo']:.3f} | {c['ic95'][0]:.3f}–{c['ic95'][1]:.3f} | "
                          f"{c['series_abaixo_de_1']} de {c['n_series']} | {leitura(nome, c['ic95'])} |")
    linhas += ["", "Leitura conforme a seção 3 do plano. Para porta ÷ referência (C01, C03, C04), a margem de 1% do D04 só é "
               "confirmada se o limite superior for <= 1,01. Limites do método: seção 4 do plano (séries tratadas como "
               "independentes; intervalos tendem a ser estreitos demais quando as séries compartilham o tempo)."]
    (AQUI / "INCERTEZA_RESULTADO.md").write_text("\n".join(linhas) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(linhas))


if __name__ == "__main__":
    if "--resumo" in sys.argv:
        resumo()
    else:
        for f in sys.argv[1:]:
            familia(f)
