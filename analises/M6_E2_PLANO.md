# Medição M6_E2 (v0.54, M6 rascunho 1): plano e critérios, escritos e commitados antes de rodar

**Data:** 11/10/2026. **Para quê:** conferir no banco a M6 rascunho 1 (`ALGORITHM_SPEC_DRAFT_M6.md` no lebre-research,
commit `0cf9828`), revista depois da M6_E1 (`M6_E1_RESULTADO.md`): candidatos 7, 24 e 168, o de menor período primeiro, e
teste só depois de 10 visitas por fase. O banco já foi visto pela M6; esta medição só decide se o rascunho 1 segue para
validação em dados novos.

**Código:** protótipo no commit `18906c2` (git worktree fixo). Script: `analises/m6_e2.py` (cópia de `m6_e1.py`; mudanças
declaradas no cabeçalho), com as mesmas três rodadas (a), (b) e (c). Banco: as 64 famílias do E20. Bootstrap como na
M6_E1, semente 20261343 (conferida como não usada).

## Critérios (os da M6_E1, sem mudança)

1. **Sem piora com o ciclo declarado:** em cada família, (a) com limite superior do IC 95% ≤ 1,01; nenhuma previsão não
   finita.
2. **Sem declarar, D02:** razão (b) (média geométrica) ≤ 1,05 em B01 e em B02.
3. **Nenhum ciclo falso:** nenhuma série de A02 com ciclo aceito; no máximo 5% das séries de A01 a A12.

**Regra:** se atender a 1, 2 e 3, a M6 (rascunho 1) segue para validação em dados novos; se não, as falhas são declaradas
e nada é ajustado.
