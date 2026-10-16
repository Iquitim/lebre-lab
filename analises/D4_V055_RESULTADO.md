# D4 da v0.55 — resultado

**Plano:** `analises/D4_V055_PLANO.md` (commit `4f19e43`, antes de rodar). **Protótipo:** lebre-research `2f250bf`, num
worktree fixo. **Execução:** única, 16/10/2026, depois do ensaio. Saídas: `d4_v055/sint.json` e `d4_v055/resumo.json`.

No script e no `resumo.json`, os critérios D4-a, D4-b, D4-d, D4-e, D4-f e D4-g aparecem com os rótulos herdados
"D2-a" a "D2-g", como o plano declara.

## Decisão pela regra pré-registrada

| Critério | B8 (candidata) | B7 (comparador) |
|---|---|---|
| D4-a espúrias em séries integradas | passa | passa |
| D4-b nulos estacionários | passa | passa |
| D4-d retenção | **passa** (P6: 54/60 contra 50/60 da v0.54) | passa |
| D4-e atraso | passa | passa |
| D4-f precisão (todo limite superior ≤ 1,02) | **falha: W4, 1,360 (1,346–1,374)** | falha: P3, 1,026 |
| D4-g custo | passa (mediana 1,039) | passa (1,060) |
| D4-h a informação chega à previsão (P3 e P6) | **passa:** P3 0,965 (0,955–0,975); P6 0,966 (0,952–0,978) | falha (P3, IC até 1,026) |
| D4-i P6: espúrias no fim | passa (0/60) | passa (0/60) |

**B8 não passa.** O resultado negativo é registrado.

## O que aconteceu (descritivo, depois de ver os resultados)

Unidade "passado do alvo" na estrutura final:

| Célula | A | B7 | B8 |
|---|---|---|---|
| W4 tipo solar (40) | 40 | 40 | **0** |
| P6 (60) | 47 | 53 | **0** |
| P3 (60) | 43 | 40 | 12 |
| W1, W2, W3 (40 cada) | 4, 6, 10 | 5, 7, 9 | 2, 3, 6 |

**O portão se trava sozinho.** No começo da série, a estrutura de nível ainda não aprendeu e wS fica abaixo de 0,05. O
portão bloqueia justamente a unidade interna que faria s melhorar, e wS nunca sobe.
- **Em séries integradas (P3, P6),** isso não custa nada. Libera as vagas para a entrada verdadeira, e é por isso que
  D4-d e D4-h passaram com folga.
- **Com memória fraca (W4),** é exatamente a unidade que precisava entrar: +36% de erro.

A regra "gastar só onde há uso" falha quando o "uso" depende da própria decisão.

**O que se aprendeu nas rodadas D1 a D4, em sintéticos:**

| Peça | Efeito | Status |
|---|---|---|
| Entradas externas testadas contra a previsão do núcleo | espúrias em séries integradas: 27–33 de 60 → 0, em todas as rodadas; sem custo de precisão | robusto |
| Unidades internas testadas contra s (B6) | corrige a perda de memória fraca de B4 | robusto (D2, D3) |
| Estrutura de inovação aninhada (B7) | a informação da entrada verdadeira chega à previsão em série integrada | parcial: P3 0,984 na D3, mas IC até 1,026 na D4 |
| Portão de testes internos por wS (B8) | libera vagas em série integrada (P3, P6: ganho de 3,5%) | **rejeitado:** trava com memória fraca |

**Hipótese para um próximo desenho (não testada).** Um portão que não dependa da própria decisão. Por exemplo:
- bloquear testes internos só quando a estrutura de **inovação** carrega a previsão (wI alto, o sinal de série
  integrada), e não quando wS é baixo;
- ou deixar passar uma unidade interna com triagem muito forte, acima de um múltiplo do limiar.
