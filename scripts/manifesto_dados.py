"""Manifesto dos dados do LEBRE Lab: caminho, tamanho, data de gravação e SHA-256 de cada arquivo em dados/.

Uso: python scripts/manifesto_dados.py            grava dados/MANIFESTO_SHA256.tsv
     python scripts/manifesto_dados.py --conferir  compara os arquivos atuais com o manifesto (sai com 1 se divergir)

Os dados brutos não entram no git; o manifesto entra. lab/run.py registra o SHA-256 do manifesto em cada execução.
"""
import datetime as dt
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / "dados"
MAN = DADOS / "MANIFESTO_SHA256.tsv"
FORA = {"MANIFESTO_SHA256.tsv", "FONTES.md"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def linhas():
    for p in sorted(DADOS.rglob("*")):
        if p.is_file() and p.name not in FORA:
            st = p.stat()
            yield p.relative_to(ROOT).as_posix(), st.st_size, dt.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"), sha(p)


def main():
    atual = list(linhas())
    if "--conferir" in sys.argv:
        ref = {l.split("\t")[0]: l.split("\t")[3] for l in MAN.read_text(encoding="utf-8").splitlines()[1:]}
        div = [c for c, _, _, h in atual if ref.get(c) != h] + [c for c in ref if c not in {a[0] for a in atual}]
        print(f"{len(atual)} arquivos; divergências: {len(div)}"); [print("  ", d) for d in div]
        sys.exit(1 if div else 0)
    txt = "caminho\tbytes\tgravado_em\tsha256\n" + "".join("\t".join(map(str, l)) + "\n" for l in atual)
    MAN.write_text(txt, encoding="utf-8", newline="\n")
    print(f"{len(atual)} arquivos; manifesto SHA-256 {hashlib.sha256(txt.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
