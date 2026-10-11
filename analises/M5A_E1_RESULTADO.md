# Medição M5A_E1: resultado

Plano `M5A_E1_PLANO.md`.

Protótipo: commit `86bf359`.

## 1. Custo da M1 (FP por passo)

| Cenário | v0.53 | v0.54 | razão | critério (≤ 0,25) | total v0.53 | total v0.54 |
|---|---|---|---|---|---|---|
| A01 | 819 | 467 | 0.570 | não atende | 2681 | 2329 |
| A05 | 401 | 85 | 0.211 | atende | 924 | 607 |
| C03 | 725 | 545 | 0.751 | não atende | 1453 | 1272 |

## 2. Sem piora nas famílias do E20 (64 de 64)

- famílias com limite superior > 1,01: []
- maior limite superior: YB03 1.0037 (razão 0.9981)
- previsões não finitas: 0
- séries em que a M1 dormiu: 476 de 728
- identidade onde nunca dormiu: ok

## 3a. Troca de regime

- MSE depois da troca, v0.54 ÷ v0.53 (geo, 20): 1.0000 → atende

## 3b. Útil → inútil → útil

- séries na condição (v0.53 volta a pesar e a v0.54 dormiu antes): 20
- fração que desperta: 1.0 → atende
- MSE do último trecho, v0.54 ÷ v0.53 (geo, 20): 0.9671 → atende

## Decisão pela regra do plano

A M5a (rascunho 0, revisão a) **não é aceita**: reprova no critério 1 (custo) em A01 (razão 0,570) e C03 (0,751);
atende a 2, 3a, 3b e 5. Nada foi ajustado.

## Diagnóstico (descritivo, depois do resultado)

- **Desvio do protótipo em relação à especificação (declarado):** o protótipo desperta a M1 quando a seleção de entradas
  muda (`dormancy.py`, `_select`); essa regra **não estava no rascunho 0**. Instrumentando a causa dos despertares, sem
  mudar o comportamento: em A01, 3 de 3 despertares por série vêm da nova seleção (feita a cada 5.000 alvos; com 10 a 50
  entradas candidatas, o conjunto escolhido muda); em A12, 36 de 39. Cada despertar custa a sombra de 100 atualizações e
  mais 2.000 alvos no modo ativo antes de dormir de novo.
- **C03:** as séries têm ~4.000 passos; com a sombra e os 2.000 alvos exigidos antes de dormir, a M1 fica dormente
  ~1.100 passos por série.
- Nas séries solares e de carga com mais despertares (5 a 6 por série), todos vieram da estatística de despertar.
- Nas 654 séries do E20 com M1, a razão de custo da M1 v0.54 ÷ v0.53 teve mediana 0,68 (0,485 entre as 476 em que ela
  dormiu); 78 séries tiveram 3 ou mais despertares.
- **3b:** a v0.54 errou 3,3% menos que a v0.53 no último trecho: depois do despertar, o AdaHedge reiniciado devolve peso
  à M1, enquanto o da v0.53 carrega a desvantagem acumulada.
