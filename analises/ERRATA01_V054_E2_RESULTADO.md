# Errata 01 da v0.54, segunda medição (dados novos): resultado

Plano `ERRATA01_V054_E2_PLANO.md`. 60 séries sintéticas novas.

| Grupo | séries | pico v0.53 | pico v0.54 promovida | pico v0.54 com errata | errata ÷ v0.53 | maior diferença de custo (critério 2) |
|---|---|---|---|---|---|---|
| custo_d10 | 10 | 6349 | 6584 | 6419 | 1.011 | 0.00e+00 |
| custo_d20 | 10 | 6667 | 7417 | 6787 | 1.018 | 7.45e-09 |
| custo_d50 | 10 | 7849 | 11944 | 8269 | 1.054 | 7.45e-09 |
| troca | 10 | 3168 | 3169 | 3151 | 0.995 | 0.00e+00 |
| intermitente | 10 | 2188 | 2155 | 2151 | 0.983 | 0.00e+00 |
| nulo_d20 | 10 | 6583 | 7333 | 6703 | 1.018 | 7.45e-09 |

1. **Identidade com a v0.54 promovida:** atende
2. **Custo total igual, contando as linhas pendentes no fim:** atende
3. **Pico ≤ 1,10 × o da v0.53 em cada grupo:** atende

**Decisão pela regra do plano:** a errata 01 é **aceita**.

**Nota de execução:** o processo do grupo `custo_d50` foi interrompido em 8 de 10 séries pelo encerramento da sessão de
trabalho, antes de gravar o arquivo do grupo. O grupo foi rodado de novo do início, com o mesmo código; as 8 séries da
passada interrompida (registradas no log) são idênticas às da nova passada. Nada mais foi refeito.
