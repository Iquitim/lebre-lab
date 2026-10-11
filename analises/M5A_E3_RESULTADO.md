# Medição M5A_E3 (M5a rascunho 2): resultado

Plano `M5A_E3_PLANO.md`. Critério 1 só em A01 e A05; C03 reportado.

Protótipo: commit `f69dec4`.

## 1. Custo da M1 (FP por passo)

| Cenário | v0.53 | v0.54 | razão | critério (≤ 0,25) | total v0.53 | total v0.54 |
|---|---|---|---|---|---|---|
| A01 | 819 | 305 | 0.373 | não atende | 2681 | 2167 |
| A05 | 401 | 85 | 0.211 | atende | 924 | 607 |
| C03 | 725 | 545 | 0.751 | só reportado | 1453 | 1272 |

## 2. Sem piora nas famílias do E20 (64 de 64)

- famílias com limite superior > 1,01: []
- maior limite superior: YB03 1.0043 (razão 0.9998)
- previsões não finitas: 0
- séries em que a M1 dormiu: 476 de 728
- identidade onde nunca dormiu: ok

## 3a. Troca de regime

- MSE depois da troca, v0.54 ÷ v0.53 (geo, 20): 1.0000 → atende

## 3b. Útil → inútil → útil

- séries na condição (v0.53 volta a pesar e a v0.54 dormiu antes): 18
- fração que desperta: 1.0 → atende
- MSE do último trecho, v0.54 ÷ v0.53 (geo, 20): 0.8324 → atende

- Critério 1 (A01 e A05): não atende

## Decisão pela regra do plano

A M5a (rascunho 2) **não é aceita**: reprova no critério 1 em A01 (0,373 > 0,25); atende a 2 (nenhuma família acima de
1,01; YB03 com limite superior 1,0043), 3a, 3b e 5. Nada foi ajustado.

## Comparação dos três desenhos (descritiva)

| | Rascunho 0 (rev. a) | Rascunho 1 | Rascunho 2 |
|---|---|---|---|
| Custo da M1, A01 (meta ≤ 0,25) | 0,570 | 0,264 | 0,373 |
| Custo da M1, A05 | 0,211 | 0,211 | 0,211 |
| Pior família (limite superior; meta ≤ 1,01) | YB03 1,0037 | YB03 1,0216 | YB03 1,0043 |
| YB03, série NO2 | 1,0042 | 1,0502 | 1,0042 |
| Custo da M1 nas séries do E20 (mediana da razão) | 0,680 | 0,659 | 0,674 |
| 3b, último trecho (v0.54 ÷ v0.53) | 0,967 | 0,926 | 0,832 |

O rascunho 2 é o único dos três que atende a todos os critérios de precisão e identidade; a meta de custo de 75% em A01
(séries de 20.000 passos, com reseleção de entradas a cada 5.000 alvos) não foi atingida por nenhum desenho que preserva
o ganho de YB03.
