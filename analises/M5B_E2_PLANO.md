# Medição M5B_E2 (v0.54, M5b rascunho 1): plano e critérios, escritos e commitados antes de rodar

**Data:** 11/10/2026. **Para quê:** conferir a M5b rascunho 1 (`ALGORITHM_SPEC_DRAFT_M5b.md` no lebre-research, commit
`e2654a1`) no banco: passo 31 (primo) em vez de 32 na atualização da matriz de covariâncias das entradas, depois do
aliasing encontrado na M5B_E1 (`M5B_E1_RESULTADO.md`). O banco já foi visto pela M5b; por isso esta medição só decide se
o rascunho 1 segue para validação em dados novos.

**Código:** protótipo no commit `438ac08` (git worktree fixo); `Lebre054` com `m5b=False` contra `m5b=True`, mesmos
argumentos da M5B_E1. Script: `analises/m5b_e2.py` (cópia de `m5b_e1.py` com as mudanças declaradas no cabeçalho).
**Banco:** as 64 famílias do E20, todas as séries.

## Critérios (os da M5B_E1, com o critério 2 reescrito depois dela, declarado)

1. **Identidade:** em todas as séries, previsões idênticas passo a passo (NaN igual a NaN) e estrutura final idêntica.
2. **Custo:** custo do núcleo nunca maior. Menor em toda série em que a triagem roda (custo de triagem do original > 0).
   Razão ≤ 0,80 na média do grupo d = 50 de A01 e em A12.
3. **Relatório de equivalentes:** no fim de cada série, fora da faixa 0,90 ≤ |r| ≤ 0,98 (correlação estimada pelo
   original), a pertinência é a mesma nos dois. Dentro da faixa, só reportada.

**Regra:** se atender a 1, 2 e 3, a M5b (rascunho 1) segue para validação em dados novos; se não, as falhas são declaradas
e nada é ajustado.
