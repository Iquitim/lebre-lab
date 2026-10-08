"""Diagnóstico (plano: diagnosticos/M1_VAL4_ATRIBUICAO_PLANO.md): m1_val4 com a M2 sem a M1. Só descrição."""
import sys
from pathlib import Path

from analises import m1_val4 as V
from analises import m2_dev as M

_orig = M.Lebre053


def _sem_m1(*a, **k):
    k["precisao"] = False
    return _orig(*a, **k)


M.Lebre053 = _sem_m1
V.SAIDA = Path(__file__).with_name("m1val4_sem_m1")

if __name__ == "__main__":
    for f in sys.argv[1:]:
        V.familia(f)
