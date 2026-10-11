# Medição M4_E1 (v0.54, M4 rascunho 0): plano e critérios, escritos e commitados antes de rodar

**Data:** 11/10/2026. **Para quê:** decidir se a M4 rascunho 0 (`ALGORITHM_SPEC_DRAFT_M4.md` no lebre-research, commit
`e2654a1`) segue para validação em dados novos. A M4 muda só o ciclo de vida das remoções: evidência nova por episódio,
orçamento e-LOND próprio, teste aberto quando a contribuição da unidade cai à metade da referência, episódio de até
10.000 passos.

**Código:** protótipo no commit `438ac08` (git worktree fixo); `Lebre054` com `m4=False` contra `m4=True`, os dois com a
M5a e sem a M5b, mesmos argumentos de cada série das medições da M5a. Script: `analises/m4_e1.py`.
**Banco:** as 64 famílias do E20, todas as séries. Bootstrap de blocos pareado como no E20 (blocos de 168 nas famílias
B, 12 em C05, 20 nas demais; nas curtas, como no E20), semente 20261340 (conferida como não usada).

## Critérios (fixados antes; os do rascunho 0)

1. **A05:** entrada antiga (x0) removida entre a troca (passo 15.000) e 10.000 passos depois, em pelo menos 14 de 20
   séries.
2. **Sem remoções falsas:** em A01 (30 séries), nenhuma remoção de x0 ou x1. Em A02, nenhuma série com entrada externa na
   estrutura final.
3. **Sem piora:** em cada família, razão de MSE com M4 ÷ sem M4 (média geométrica das séries), limite superior do IC 95%
   ≤ 1,02; nenhuma previsão não finita no trecho avaliado (depois de 20% da série).
4. **Identidade:** onde nenhuma unidade foi aceita sem a M4, previsões idênticas.

Reportados sem critério: C03 (entradas externas na estrutura final, com e sem M4, e aceitas em algum momento), remoções
por família e custo total.

**Regra:** se atender a 1 a 4, a M4 (rascunho 0) segue para validação em dados novos; se não, as falhas são declaradas e
nada é ajustado.
