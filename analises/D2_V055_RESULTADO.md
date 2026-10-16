# D2 da v0.55 — resultado

**Plano:** `analises/D2_V055_PLANO.md` (commit `c059587`, antes de rodar). **Protótipo:** lebre-research `e375ec4`, num
worktree fixo. **Execução:** única, 16/10/2026, depois do ensaio. Saídas: `d2_v055/sint.json` e `d2_v055/resumo.json`.

## Decisão pela regra pré-registrada

**Checagem de validade do banco: válido.** Na célula W4 (tipo solar), B4 ÷ A = 1,066 (IC 1,046–1,089): o mecanismo da
falha da D1 foi reproduzido.

| Critério | B6 (candidata) | B4 (comparador) |
|---|---|---|
| D2-a espúrias em séries integradas | passa | passa |
| D2-b nulos estacionários | passa | passa |
| D2-d retenção do genuíno | **falha: P3, 50/60 contra 55/60 da v0.54** (mínimo 52) | passa |
| D2-e atraso de detecção (P1) | passa (935 contra 920) | passa |
| D2-f precisão (todo limite superior ≤ 1,02) | **passa** (pior: P3, 1,007) | falha (W4, 1,089) |
| D2-g custo | passa (mediana 1,000) | passa |

**B6 não passa.** O resultado negativo é registrado.

## Por célula

Cada célula mostra:
- séries com entrada externa no fim;
- x0 no fim;
- a razão de MSE contra a v0.54, com IC 95% pelas séries.

| Célula | A (v0.54) | B4 | B6 |
|---|---|---|---|
| N1 passeios + entradas que passeiam (60) | **33** externas | 0; razão 1,000 | 0; razão 1,000 |
| N2 (60) | 0 | 0 | 0 |
| N3, N4, N5 nulos (80 cada) | 0 alguma vez | 0 | 0 (N4: 1,000) |
| P1 / P2 (60) | x0 60 / 60 | 60 / 60 | 60 / 60 |
| P3 I(1), entrada nas diferenças (60) | x0 55 | 52; 1,003 (0,999–1,008) | **50**; 1,002 (0,998–1,007) |
| P4 cointegração (60) | x0 56 | 58 | 59 |
| W1 ciclo declarado errado + entrada (40) | x0 2 | 0; 1,002 | 1; 1,001 |
| W2 ciclo errado, sem entrada (40) | — | 1,003 (0,999–1,007) | 0,999 |
| W3 ciclo não declarado + entrada (40) | x0 1 | 0,999 | 1,000 |
| W4 tipo solar (40) | — | **1,066 (1,046–1,089)** | **0,993 (0,988–0,997)** |

## Diagnóstico (descritivo, depois de ver os resultados; não muda a decisão)

**P3, as 8 séries em que a v0.54 retém x0 e B6 não.** Em 6 delas, a sequência foi a mesma:
- B6 aceita x0 entre os passos 2.190 e 3.020;
- depois, um teste periódico de remoção, contra a previsão do núcleo, a aceita entre os passos 6.160 e 6.830, com cerca
  de 4.000 amostras de evidência;
- em todas, o peso médio da estrutura no núcleo é 0,0: a previsão é a memória.

**Leitura:**
- Numa série integrada, a estrutura modela o **nível** e perde para a memória (wS ≈ 0).
- Tirar x0 dessa estrutura não muda a previsão do núcleo. Contra ela, a remoção está correta.
- A v0.54 retém x0 numa estrutura que a previsão também não usa: a precisão das duas é igual nessa célula (1,002).
- O critério D2-d mede retenção estrutural, não informação na saída.
- O que a D2 revela é um **limite comum às duas versões:** numa série integrada, a informação de uma entrada verdadeira
  sobre as diferenças não chega à previsão.

**O que a D2 confirma de positivo, com sementes novas e banco válido:**
- B6 elimina as entradas externas espúrias em séries integradas (33/60 → 0/60);
- B6 corrige a perda de B4 em memória fraca (W4: 0,993 contra 1,066);
- B6 não piora a precisão em nenhuma das 13 células.

**Hipótese para um próximo desenho (não testada).** Acrescentar ao núcleo um terceiro especialista: a estrutura sobre a
inovação da memória (a cascata). A combinação seria pela mesma média dinâmica, sem substituir a estrutura de nível.
- A fumaça mostrou que a cascata perde onde precisa cancelar yₜ₋₁ (estacionário com entrada).
- Em série integrada, ela não precisa cancelar nada: a inovação já é Δy.
- A média dinâmica escolheria, série a série.
- Custo esperado: mais um conjunto de pesos de estrutura.

## Errata (16/10/2026, registrada no plano da D3, antes de rodá-la)

No ensaio, a base de sementes 2026101690 + c, com c = 10 a 12, coincidiu com as sementes das séries k = 0 de N1, N2 e N3
da execução principal (2026101700 a 2026101702). Houve, portanto, reuso de semente entre o ensaio e a execução. O
resultado não muda: o ensaio não foi usado, e as células geram séries diferentes.
