"""Montagem da validação 7 (regras: analises/VALIDACAO7_PLANO.md). Só metadados: baixa os dados das famílias reais U,
registra o SHA-256 de cada arquivo lido (dados/VALIDACAO7_SHA256.tsv) e lista as séries (nome, passos, cobertura do alvo).
Nenhuma previsão. Rodar da raiz do Lab:  python -m analises.montar_validacao7
"""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

from lab import fontes as F
from lab import usinas as U
from lab.run import ROOT, load

LIDOS = set()
_get_orig = F._get


def _get(url, dest, *a, **k):
    LIDOS.add(Path(dest).resolve())
    return _get_orig(url, dest, *a, **k)


F._get = _get
FAMILIAS = ["TB03_qualidade_do_ar", "TB06_eolica"]


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def anteriores():
    vistos = {}
    for m in sorted((ROOT / "dados").glob("*SHA256*.tsv")):
        if m.name == "VALIDACAO7_SHA256.tsv":
            continue
        for r in csv.DictReader(open(m, encoding="utf-8"), delimiter="\t"):
            vistos[r["caminho"]] = r["sha256"]
    return vistos


def main():
    series = []
    for f in FAMILIAS:
        mod = load(ROOT / "scenarios" / "T" / f"{f}.py")
        for i in mod.SPEC["sementes"]:
            s = mod.gerar(i)
            y = np.asarray(s["y"], float)
            series.append(dict(familia=mod.SPEC["id"], serie=s["nome"], passos=len(y), d=int(np.asarray(s["X"]).shape[1]),
                               cobertura_alvo=round(float(np.isfinite(y).mean()), 4)))
            print(series[-1], flush=True)
    if U.CACHE.exists():
        LIDOS.add(U.CACHE.resolve())
    vistos = anteriores()
    linhas = []
    for p in sorted(LIDOS):
        rel = p.relative_to(ROOT).as_posix()
        h = _sha(p)
        origem = "novo (validação 7)" if rel not in vistos else ("compartilhado, hash idêntico" if vistos[rel] == h else "MUDOU")
        linhas.append(dict(caminho=rel, tamanho=p.stat().st_size, sha256=h, origem=origem))
    mudou = [l for l in linhas if l["origem"] == "MUDOU"]
    out = ROOT / "dados" / "VALIDACAO7_SHA256.tsv"
    with open(out, "w", newline="\n", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["caminho", "tamanho", "sha256", "origem"], delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(linhas)
    # conferência: os arquivos dos manifestos anteriores continuam iguais
    alterados = [c for c, h in vistos.items() if (ROOT / c).exists() and _sha(ROOT / c) != h]
    resumo = dict(series=series, n_arquivos=len(linhas), novos=sum(l["origem"].startswith("novo") for l in linhas),
                  compartilhados=sum(l["origem"].startswith("compartilhado") for l in linhas), mudou=[l["caminho"] for l in mudou],
                  manifestos_anteriores_alterados=alterados, sha256_manifesto=_sha(out))
    (ROOT / "analises" / "validacao7_montagem.json").write_text(json.dumps(resumo, indent=1, ensure_ascii=False) + "\n",
                                                               encoding="utf-8", newline="\n")
    print({k: v for k, v in resumo.items() if k != "series"})


if __name__ == "__main__":
    main()
