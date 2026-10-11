# Medição M4_E2 (v0.54, M4 rascunho 1): plano e critérios, escritos e commitados antes de rodar

**Data:** 11/10/2026. **Para quê:** conferir no banco a M4 rascunho 1 (`ALGORITHM_SPEC_DRAFT_M4.md` no lebre-research,
commit `3012638`), revista depois da M4_E1 (`M4_E1_RESULTADO.md`): o teste de remoção disparado é acrescentado ao
calendário original (com prioridade) e só aceita depois de 5.000 passos de evidência. O banco já foi visto pela M4; esta
medição só decide se o rascunho 1 segue para validação em dados novos.

**Código:** protótipo no commit `cfe72ce` (git worktree fixo); `Lebre054` com `m4=False` contra `m4=True`, os dois com a
M5a e sem a M5b. Script: `analises/m4_e2.py` (cópia de `m4_e1.py`; mudanças declaradas no cabeçalho). Banco: as 64
famílias do E20. Bootstrap como na M4_E1, semente 20261342 (conferida como não usada).

## Critérios (os da M4_E1, sem mudança)

1. **A05:** x0 removida entre a troca e 10.000 passos depois, em pelo menos 14 de 20 séries.
2. **Sem remoções falsas:** A01, nenhuma remoção de x0 ou x1; A02, nenhuma série com entrada externa na estrutura final.
3. **Sem piora:** em cada família, limite superior do IC 95% da razão de MSE ≤ 1,02; nenhuma previsão não finita.
4. **Identidade:** onde nenhuma unidade foi aceita sem a M4, previsões idênticas.

Reportados: C03, remoções por família, custo.

**Regra:** se atender a 1 a 4, a M4 (rascunho 1) segue para validação em dados novos; se não, as falhas são declaradas e
nada é ajustado.
