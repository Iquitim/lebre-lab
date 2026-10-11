"""Medição M5A_E3 (plano: analises/M5A_E3_PLANO.md): M5a rascunho 2. Reusa analises/m5a_e1.py sem alteração; troca só as
sementes, a pasta de saída e o critério de custo (A01 e A05; C03 reportado).

Uso (da raiz do Lab, com LEBRE054_PROTO no worktree do commit f69dec4 e LEBRE053_PROTO como no M5A_E1):
  python -m analises.m5a_e3 custo | cenarios | familias FAM ... | resumo
"""
import sys

from analises import m5a_e1 as E

E.OUT = E.AQUI / "m5a_e3"
E.SEMENTE_BOOT = 20261062
E.SEM_3A = list(range(20261152, 20261172))
E.SEM_3B = list(range(20261172, 20261192))
CUSTO_CRITERIO = ("A01", "A05")


def resumo():
    import json
    e1 = E.AQUI / "M5A_E1_RESULTADO.md"
    guardado = e1.read_bytes()                                      # o resumo do E1 grava neste arquivo: preservar
    try:
        E.resumo()
        txt = e1.read_text(encoding="utf-8")
    finally:
        e1.write_bytes(guardado)
    c = json.loads((E.OUT / "custo.json").read_text(encoding="utf-8"))
    ok = all(c[k]["atende"] for k in CUSTO_CRITERIO)
    txt = txt.replace("# Medição M5A_E1: resultado", "# Medição M5A_E3 (M5a rascunho 2): resultado")
    txt = txt.replace("Plano `M5A_E1_PLANO.md`.", "Plano `M5A_E3_PLANO.md`. Critério 1 só em A01 e A05; C03 reportado.")
    txt += f"\n- Critério 1 (A01 e A05): {'atende' if ok else 'não atende'}\n"
    (E.AQUI / "M5A_E3_RESULTADO.md").write_text(txt, encoding="utf-8", newline="\n")
    print(txt)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "custo":
        E.custo()
    elif cmd == "cenarios":
        E.cenarios()
    elif cmd == "familias":
        for f in sys.argv[2:] or E.E20.TODAS:
            E.familia(f)
    elif cmd == "resumo":
        resumo()
