# Banco fixo da v0.55 — rodada D5: resultado

**Plano:** `analises/BANCO_V055_PLANO.md`, com a rodada D5 registrada no commit `9f48971`, antes de rodar.
**Protótipo:** lebre-research `b0522a0`, num worktree fixo. **Execução:** única, 17/10/2026, depois do ensaio. Saídas:
`banco_v055_D5/sint.json` e `banco_v055_D5/resumo.json`.

## Decisão

| Critério | B10 (candidata) | B9 |
|---|---|---|
| C-a espúrias (N1, N2, passeios da Q7) | passa | passa |
| C-b nulos | passa | passa |
| C-d retenção | **passa** (nenhuma célula abaixo de A − 0,05) | falha (Q1) |
| C-e atraso | passa | passa |
| C-f precisão (todo limite superior ≤ 1,02) | passa (pior: N4, 1,007) | passa |
| C-g custo | passa (mediana 1,043) | passa (1,049) |
| C-h a informação chega à previsão | passa: P3 0,959 (até 0,970); P6 0,964 (até 0,973); conjunto 0,914 (0,909–0,919) | passa |

**B10 passa em todos os critérios.** Pelo processo do plano (§3), ela fica congelada no commit `b0522a0`, sem nenhuma
mudança, e vai para a confirmação C1, com sementes nunca usadas. B9 não passa (retenção na Q1).

## Por célula

Cada célula mostra:
- séries com entrada externa no fim / retenção das verdadeiras;
- a razão de MSE contra a v0.54 (IC 95%).

| Célula | A (v0.54) | B10 |
|---|---|---|
| N1 / N2 | 27 / 2 externas | 0 / 0; razão 1,000 |
| N3, N4, N5 | 0 | 0; 1,001, 1,005, 1,000 |
| P1 / P2 | 60 / 60 | 60 / 60; 1,000 / 1,001 |
| P3 | ret 57 | ret 60; **0,959 (0,948–0,970)** |
| P5 | ret 60 | ret 60; 0,993 (0,971–1,009) |
| P6 | ret 54 | ret 60; **0,964 (0,953–0,973)** |
| W1, W2, W3 | — | 1,001, 1,004, 1,001 |
| W4 | — | **0,953 (0,942–0,963)** |
| Q1 integrada sazonal | ret 38 | ret 40; **0,888** |
| Q2 AR(2) forte | ret 40 | ret 40; **0,931** |
| Q3 troca de regime | ret 40 | ret 40; **0,823** |
| Q4 intermitente | ret 35 | ret 40; **0,863** |
| Q5 duas verdadeiras (80 pares) | ret 39 | ret **74**; 0,970 |
| Q6 caudas pesadas | ret 37 | ret 40; 0,964 |
| Q7 dez entradas | ret 29; **23 com passeio no fim**; 15 com isca | ret 37; **0 com passeio**; 5 com isca; **0,675** |
| Q8 quase integrada | ret 40 | ret 40; 0,983 |

## Leitura

- As células Q1 a Q8 foram desenhadas antes de qualquer rascunho rodar nelas. Os ganhos aparecem nelas também.
- O maior, na Q7, combina três efeitos:
  - as entradas espúrias deixam de entrar (os passeios);
  - a entrada verdadeira é descoberta mais vezes;
  - a informação dela chega à previsão.
- Esta é uma rodada de **desenvolvimento**. A confirmação é a C1.
