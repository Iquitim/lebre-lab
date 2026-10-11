# Medição M5B_E1 (v0.54, M5b rascunho 0): plano e critérios, escritos e commitados antes de rodar

**Data:** 11/10/2026. **Para quê:** decidir a M5b (rascunho 0, `ALGORITHM_SPEC_DRAFT_M5b.md` no lebre-research, commit
`7e055a5`): a matriz de covariâncias das entradas, que serve só ao relatório de entradas equivalentes, passa a ser
atualizada a cada 32 passos em vez de 4, com o peso escalado para manter a janela de tempo. Previsões e decisões devem
ficar idênticas, o custo deve cair e o relatório pode mudar só perto do limiar de 0,95.

**Código:** protótipo `experiments/LEBRE-V0.54-PROTO-01` no commit `cfb0321` (git worktree fixo). Compara `Lebre054` com
`m5b=False` (a v0.54 com a M5a aceita) contra `m5b=True`, com os mesmos argumentos usados nas medições da M5a (ciclo,
segundo ciclo e referência de cada série). Script: `analises/m5b_e1.py`.

**Banco:** as 64 famílias do E20, todas as séries, como nas medições da M5a. Nenhuma semente nova: não há bootstrap,
porque a comparação de previsões é exata.

## Critérios (fixados antes)

1. **Identidade:** em todas as séries, previsões idênticas passo a passo (NaN igual a NaN) e estrutura final idêntica.
2. **Custo:** custo do núcleo por passo menor com a M5b em todas as séries. Na média do grupo d = 50 de A01 e em A12,
   razão ≤ 0,80. O custo total é reportado.
3. **Relatório de equivalentes:** no fim de cada série, para cada entrada aceita u e cada outra entrada j com correlação
   estimada pelo original fora da faixa 0,90 ≤ |r| ≤ 0,98, a pertinência de j aos equivalentes de u é a mesma nos dois.
   Dentro da faixa, a discordância é só reportada.

**Regra:** a M5b (rascunho 0) é **aceita** se atender a 1, 2 e 3. Se não, as falhas são declaradas e nada é ajustado.
