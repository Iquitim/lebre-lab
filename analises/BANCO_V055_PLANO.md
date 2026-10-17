# Banco fixo da v0.55: plano (commitado antes de qualquer rodada nele)

**Data:** 17/10/2026. **Script:** `analises/banco_v055.py`.

**Por que um banco fixo.** As medições D1 a D4 foram feitas rascunho a rascunho, cada uma com células escolhidas depois
da anterior. Isso cria o risco de ajustar o desenho aos próprios cenários. A partir daqui, valem três regras:
- as 23 células, as medidas e os critérios abaixo ficam **fixos** para todas as rodadas de desenvolvimento e para a
  confirmação;
- cada rodada usa sementes novas;
- uma rodada só acrescenta a sua entrada em `RODADAS` (commit do protótipo, sementes, variantes), num commit anterior à
  execução.

## 1. Células

São 23 células, com T = 8.000 salvo onde indicado. As células N1 a N5, P1 a P6 e W1 a W4 repetem as gerações da D2 a
D4 (`analises/d4_v055.py`). As células Q1 a Q8 são **novas**: foram desenhadas agora, antes de rodar qualquer rascunho
nelas.

| Célula | Geração | n | Verdadeiras |
|---|---|---|---|
| N1 | passeio + 5 entradas que passeiam (T = 4.000) | 60 | — |
| N2 | passeio + 5 entradas AR(0,95) (T = 4.000) | 60 | — |
| N3, N5 | AR(0,8) nulo; N5 com ruído ×3 na 2ª metade | 80 | — |
| N4 | AR(0,5) + sen(2πt/24), ciclo 24 | 80 | — |
| P1, P2 | 0,3·x0(t−3) + ruído; P2 com isca correlacionada | 60 | x0 |
| P3 | Δy = 0,5·x0(t−2) + 0,5·ruído | 60 | x0 |
| P4 | cointegração com x0 | 60 | (descritivo) |
| P5 | Δy = 1,0·x0(t−1) + 0,5·ruído | 60 | x0 |
| P6 | P3 + 3 entradas que passeiam | 60 | x0 |
| W1, W2, W3, W4 | memória fraca (ciclo errado, sem entrada, ciclo não declarado, tipo solar) | 40 | x0 em W1, W3, W4 |
| **Q1** | integrada sazonal: cumsum(0,5·x0(t−2) + 0,5·ruído) + sen(2πt/24), ciclo 24 | 40 | x0 |
| **Q2** | AR(2) (1,2; −0,35) + 0,3·x0(t−3) + 0,3·ruído | 40 | x0 |
| **Q3** | 1ª metade estacionária com entrada; 2ª metade integrada com entrada nas diferenças | 40 | x0 |
| **Q4** | integrada com relação nas diferenças desligada entre os passos 3.000 e 5.500 | 40 | x0 |
| **Q5** | Δy = 0,4·x0(t−2) + 0,3·x1(t−5) + 0,5·ruído | 40 | x0, x1 |
| **Q6** | Δy = 0,5·x0(t−2) + 0,3·t₃ (caudas pesadas) | 40 | x0 |
| **Q7** | 10 entradas: x0 verdadeira, x1 a x3 iscas (correlação ~0,7 com x0), x4 a x9 passeios; Δy = 0,5·x0(t−2) + 0,5·ruído | 40 | x0 |
| **Q8** | quase integrada: y = 0,99·y(t−1) + 0,3·x0(t−3) + 0,5·ruído | 40 | x0 |

**Sementes:** `default_rng([base + c, k])`, com c o índice da célula (0 a 22) e a base da rodada.

## 2. Medidas e critérios (fixos)

As medidas por série são as da D4. A precisão é a média geométrica das razões de MSE (variante ÷ A, v0.54) nos
últimos 2/3, com IC 95% por bootstrap das séries. Os IC das frações são de Clopper–Pearson.

| Código | Critério | Passa se |
|---|---|---|
| C-a | espúrias em séries integradas | N1 e N2: limite superior ≤ 0,10 em cada uma; contagem < a de A na soma; **e** Q7: séries com algum passeio (x4 a x9) no fim, limite superior ≤ 0,10 |
| C-b | nulos estacionários | N3, N4, N5: 0 de 80 com alguma entrada externa aceita |
| C-d | retenção | em cada célula com entrada verdadeira, a fração das verdadeiras no fim ≥ a de A − 0,05 (na Q5, as duas contam) |
| C-e | atraso | P1: mediana ≤ 1,5 × a de A |
| C-f | precisão | em **toda** célula, limite superior ≤ 1,02 |
| C-g | custo | mediana por série da razão de custo ≤ 1,25 |
| C-h | a informação chega à previsão | P3 e P6: limite superior < 1,00 cada; **e** o conjunto das integradas com entrada (P3, P5, P6, Q1, Q4, Q5, Q6, Q7), por bootstrap estratificado: limite superior < 1,00 |

Uma variante **passa** se cumprir todos os critérios, de C-a a C-h.

**Só descritivos:** P4, iscas da Q7, unidade do passado do alvo no fim, custo de pico.

## 3. Processo até uma v0.55

1. **Rodadas de desenvolvimento (D5, D6, …):**
   - cada uma com sementes novas e os critérios acima;
   - depois de uma falha: diagnóstico descritivo nas séries gastas, novo rascunho, nova rodada;
   - cada rodada fica registrada com o seu resultado, inclusive as negativas.
2. **Confirmação (rodada C1):**
   - quando uma candidata passar numa rodada de desenvolvimento, ela é congelada (commit);
   - uma única rodada com sementes nunca usadas e os mesmos critérios;
   - nenhuma mudança entre a rodada que passou e a C1.
   - Se a C1 falhar, ela conta como rodada de desenvolvimento, e a próxima confirmação precisa de sementes novas outra
     vez.
3. **Validação em séries reais nunca usadas:** pré-registro próprio, depois de passar na C1, com uma parte das séries
   guardadas (CAMELS-BR 170+, BDG2 145+, usinas eólicas), preservando o restante para a avaliação final da v0.55.

## 4. Rodada D5 (registrada neste mesmo commit, antes de rodar)

- **Protótipo:** lebre-research `experiments/LEBRE-V0.55-PROTO-01`, commit `b0522a0`.
- **Variantes:**
  - A (v0.54);
  - B9 (rascunho 6: portão suave pela triagem e pesos pelo resíduo aprendido);
  - **B10** (rascunho 7: B9 mais o piso de escala previsível e na escala de uma passada), a candidata principal.
- **Sementes:**
  - séries: base 2026102000 (2026102000 a 2026102022);
  - ensaio: base 2026101950;
  - bootstrap: 2026102030.

  Todas na faixa reservada e conferidas como não usadas em 17/10/2026.
