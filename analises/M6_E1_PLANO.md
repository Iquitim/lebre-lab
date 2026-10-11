# Medição M6_E1 (v0.54, M6 rascunho 0): plano e critérios, escritos e commitados antes de rodar

**Data:** 11/10/2026. **Para quê:** decidir se a M6 rascunho 0 (`ALGORITHM_SPEC_DRAFT_M6.md` no lebre-research, commit
`ee8667a`; ciclo como hipótese) segue para validação em dados novos.

**Código:** protótipo no commit `3a62898` (git worktree fixo). Script: `analises/m6_e1.py`. Por série, três rodadas:

- (a) argumentos do E20 (ciclo e referência declarados como nas medições anteriores), `m6=False` contra `m6=True`;
- (b) nas séries com ciclo declarado, `m6=True` sem ciclo e sem referência declarados (a referência vira a sazonal do
  menor ciclo aceito), contra (a) sem M6;
- (c) nas séries sem ciclo, os ciclos aceitos em (a) com M6.

**Banco:** as 64 famílias do E20, todas as séries. Bootstrap de blocos pareado como no E20, semente 20261341 (conferida
como não usada).

## Critérios (os do rascunho 0, fixados antes)

1. **Sem piora com o ciclo declarado:** em cada família, (a) com limite superior do IC 95% da razão de MSE ≤ 1,01;
   nenhuma previsão não finita no trecho avaliado.
2. **Sem declarar, D02:** razão de MSE (b) (média geométrica) ≤ 1,05 em B01 e em B02. As demais famílias com ciclo são
   reportadas.
3. **Nenhum ciclo falso:** nenhuma série de A02 com ciclo aceito; no máximo 5% das séries de A01 a A12 juntas.

Reportados: custo por passo e ciclos aceitos por família.

**Regra:** se atender a 1, 2 e 3, a M6 (rascunho 0) segue para validação em dados novos; se não, as falhas são declaradas
e nada é ajustado.
