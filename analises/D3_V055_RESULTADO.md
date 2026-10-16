# D3 da v0.55 — resultado

**Plano:** `analises/D3_V055_PLANO.md` (commit `870f00e`, antes de rodar). **Protótipo:** lebre-research `8ba6dc8`, num
worktree fixo. **Execução:** única, 16/10/2026, depois do ensaio. Saídas: `d3_v055/sint.json` e `d3_v055/resumo.json`.

No script e no `resumo.json`, os critérios D3-a, D3-b, D3-d, D3-e, D3-f e D3-g aparecem com os rótulos herdados
"D2-a" a "D2-g", como o plano declara.

## Decisão pela regra pré-registrada

| Critério | B7 (candidata) | B6 (comparador) |
|---|---|---|
| D3-a espúrias em séries integradas | passa | passa |
| D3-b nulos estacionários | passa | passa |
| D3-d retenção (≥ A − 0,05) | **falha: P6, 49/60 contra 54/60** (mínimo 51); nas outras células, passa | falha: P3, P5 e P6 |
| D3-e atraso (P1) | passa (910 contra 910) | passa |
| D3-f precisão (todo limite superior ≤ 1,02) | passa (pior: P5, 1,005) | passa |
| D3-g custo (mediana ≤ 1,25) | passa (1,063) | passa (0,999) |
| D3-h a informação chega à previsão (P3 e P5: limite superior < 1) | **falha:** P3 passa, 0,984 (0,975–0,991); P5 falha, 0,997 (0,987–1,005) | falha |
| D3-i P6: espúrias no fim (limite superior ≤ 0,10) | passa (0/60) | passa (0/60) |

**B7 não passa.** O resultado negativo é registrado.

## Por célula

Cada célula mostra:
- séries com entrada externa no fim;
- x0 no fim;
- a razão de MSE contra a v0.54, com IC 95%.

| Célula | A (v0.54) | B6 | B7 |
|---|---|---|---|
| N1 (60) | **27** externas | 0; 1,000 | 0; 1,000 |
| N2 (60) | 2 | 0 | 0 |
| N3, N4, N5 (80 cada) | 0 | 0 | 0 (N4: 1,003, de 1,002 a 1,005) |
| P1 / P2 (60) | x0 60 / 60 | 60 / 60 | 60 / 60 |
| P3 I(1), entrada nas diferenças | x0 60 | 50; 1,000 | **57; 0,984 (0,975–0,991)** |
| P4 cointegração | x0 57 | 59 | 60 |
| P5 I(1), efeito forte | x0 59 | 52; 1,000 | 59; 0,997 (0,987–1,005) |
| P6 I(1) + 3 espúrias que passeiam | x0 54, **40 séries com espúria** | x0 35, 0 espúrias | **x0 49, 0 espúrias**; 0,987 (0,977–0,996) |
| W1 a W3 | — | 1,000 a 1,001 | 0,999 a 1,002 |
| W4 tipo solar | — | 0,992 | **0,985 (0,979–0,993)** |

## Diagnóstico (descritivo, depois de ver os resultados; não muda a decisão)

**MSE médio geométrico contra o piso teórico** (variância do ruído nas diferenças, 0,25):

| Célula | v0.54 | B6 | B7 |
|---|---|---|---|
| P3 | 0,3111 | 0,3110 | 0,3060 |
| P5 | 0,2645 | 0,2645 | 0,2638 |
| P6 | 0,3221 | 0,3217 | 0,3179 |

- **P5:** a v0.54 já está a 6% do piso, e quase não havia o que ganhar. D3-h ficou mal posto para essa célula.
- **P3 e P6:** B7 leva a informação da entrada verdadeira à previsão, com IC abaixo de 1. É o primeiro rascunho a fazer
  isso.
- **P6:**
  - a v0.54 "retém" x0 em 54 séries, mas termina com entrada espúria em 40 de 60;
  - B7 retém x0 em 49 e termina com espúria em 0;
  - das 11 séries de B7 sem x0 no fim, em 10 x0 **nunca** foi aceita. A perda é de poder de descoberta na presença de
    passeios concorrentes, não de remoção.

**O que as três medições (D1 a D3) estabelecem em sintéticos:**
- testar as entradas externas contra a previsão do núcleo elimina as espúrias em séries integradas: 27 a 33 de 60 →
  0, em todas as rodadas;
- B6 e B7 não pioram a precisão em nenhuma célula;
- B7 é o único rascunho que leva informação de uma entrada verdadeira à previsão numa série integrada.

O que falta: poder de descoberta com passeios concorrentes (P6), custo cerca de 6% maior que o da v0.54, e confirmação
em séries reais.

**Hipótese (não testada) para o déficit de P6.** A triagem continua apontando os passeios. Cada passeio indicado ocupa uma
vaga de experimento por pelo menos 100 passos e entra numa recarga de 2.000, o que atrasa a vez de x0.
