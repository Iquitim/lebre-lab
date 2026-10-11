# Medição M5A_E2 (M5a rascunho 1): resultado

Plano `M5A_E2_PLANO.md`. Critério 1 só em A01 e A05; C03 reportado.

Protótipo: commit `1a7ff44`.

## 1. Custo da M1 (FP por passo)

| Cenário | v0.53 | v0.54 | razão | critério (≤ 0,25) | total v0.53 | total v0.54 |
|---|---|---|---|---|---|---|
| A01 | 819 | 216 | 0.264 | não atende | 2681 | 2078 |
| A05 | 401 | 85 | 0.211 | atende | 924 | 607 |
| C03 | 725 | 545 | 0.751 | só reportado | 1453 | 1272 |

## 2. Sem piora nas famílias do E20 (64 de 64)

- famílias com limite superior > 1,01: ['YB03']
- maior limite superior: YB03 1.0216 (razão 1.0106)
- previsões não finitas: 0
- séries em que a M1 dormiu: 476 de 728
- identidade onde nunca dormiu: ok

## 3a. Troca de regime

- MSE depois da troca, v0.54 ÷ v0.53 (geo, 20): 1.0000 → atende

## 3b. Útil → inútil → útil

- séries na condição (v0.53 volta a pesar e a v0.54 dormiu antes): 16
- fração que desperta: 1.0 → atende
- MSE do último trecho, v0.54 ÷ v0.53 (geo, 20): 0.9260 → atende

- Critério 1 (A01 e A05): não atende

## Decisão pela regra do plano

A M5a (rascunho 1) **não é aceita**: reprova no critério 1 (A01: 0,264 > 0,25) e no critério 2 (YB03: razão 1,0106,
limite superior 1,0216 > 1,01); atende a 3a, 3b e 5. Nada foi ajustado.

## Diagnóstico (descritivo, depois do resultado)

- **YB03 (qualidade do ar de Pequim), série NO2:** no rascunho 0 a troca de seleção despertava a M1 e o especialista novo
  ganhava peso (série 1,0042); no rascunho 1 a M1 ficou dormente 27.483 de 35.064 passos sem que a estatística de
  despertar (melhora ≥ 5% nas amostras) disparasse, e a série piorou 5,0% (1,0502). As outras três séries da família
  ficaram iguais ou melhores que a v0.53. Leitura: o AdaHedge aproveita vantagens pequenas do especialista (a combinação
  pode superar os dois), que a estatística de despertar, com limiar de 5% e amostra de 1 em 8, não detecta.
- **A01:** a M1 dormente custa ~110 a ~140 FP; o excesso vem dos primeiros ~2.100 passos de cada série (sombra e os 2.000
  alvos exigidos antes de dormir), sempre ativos, em séries de 20.000 passos.
- **Tensão revelada pelos dois desenhos:** os despertares por troca de seleção, que custaram caro em A01 (rascunho 0), eram
  úteis em YB03 (rascunho 1).
