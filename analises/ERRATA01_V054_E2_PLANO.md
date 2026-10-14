# Errata 01 da v0.54, segunda medição (dados novos): plano e critérios, escritos e commitados antes de rodar

**Data:** 14/10/2026. **Para quê:** a primeira medição da errata 01 (`ERRATA01_V054_RESULTADO.md`, commit `6b826cd`) não
aceitou a M5b rascunho 2 só pela redação do critério 2 ("custo médio igual"). Em 70 de 728 séries, a diferença foi
exatamente o custo das linhas da matriz ainda pendentes no fim da série (verificado em 728 de 728). O critério 2 é
reescrito aqui **depois de ver aquele resultado, e isso é declarado**. Por isso esta medição usa dados novos e é usada
uma única vez.

**Código:** o mesmo da primeira medição (protótipo `f9906c4`; v0.54 promovida reproduzida com o núcleo do commit
`cfe72ce`; v0.53 = `lebre==0.2.0`). Script: `analises/errata01_v054_e2.py`.

**Dados (60 séries sintéticas novas, sementes inteiras 2026101410 a 2026101469, conferidas como não usadas):**

| Grupo | Gerador | Séries | Sementes |
|---|---|---|---|
| custo d = 10, 20, 50 | o de A01 (`lab.synth.base_truth`), T = 20.000 | 10 por d | 2026101410 a 2026101439 |
| troca de regime | o de A05 | 10 | 2026101440 a 2026101449 |
| intermitente | o de A07 | 10 | 2026101450 a 2026101459 |
| nulo com 20 entradas | o de A02, com 20 entradas em vez de 5 | 10 | 2026101460 a 2026101469 |

## Critérios

1. **Identidade com a v0.54 promovida:** previsões idênticas passo a passo, estrutura final idêntica e relatório de
   equivalentes idêntico no fim, em todas as séries.
2. **Custo (reescrito depois da primeira medição, declarado):** custo total da série da v0.54 com errata + custo das
   linhas pendentes no fim (calculado pelo estado do modelo: soma de 3(d_c − i) das linhas que faltam aplicar) =
   custo total da v0.54 promovida, com diferença ≤ 10⁻⁶ operação, em todas as séries.
3. **Pico:** em cada grupo, o maior custo de um passo da v0.54 com errata ≤ 1,10 × o da v0.53.

**Regra:** a errata 01 é **aceita** se atender a 1, 2 e 3; se não, as falhas são declaradas e nada é ajustado.
