# Validação 5 (M1 rascunho 5 + M2 Q2), critério 2: resultado

Plano `M1_VAL5_PLANO.md`. Régua por decidibilidade com o adendo 3 de 09/10/2026 (choque > máx(5%, 5 × 2 ln(n)/n) → indecidível nos critérios 1 e 2).

## M1 rascunho 5 + M2 candidata Q2

Protótipo `bca5dac`. Famílias não medidas: nenhuma.

| Critério | Falhas |
|---|---|
| 1 | - |
| 2 | - |
| 4 | - |
| 5 | - |
| 6 | - |
| 7 | - |

**Atende aos critérios da M2.**

| Família | v0.52 melhor / ref. melhor / indecidível / choque | 1 | 2 | 7 | todas ÷ v0.52 | +custo (máx) | externas (v0.52) |
|---|---|---|---|---|---|---|---|
| ZB01 | 5 / 0 / 0 / 0 | - | 1.000 (1.000–1.000; n = 5) | - | 1.000 (1.000–1.000; n = 5) | 654 (660) | 0 (0) |
| ZB02 | 4 / 0 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 855 (870) | 4 (4) |
| ZB03 | 4 / 0 / 0 / 0 | - | 0.956 (0.938–0.973; n = 4) | - | 0.956 (0.938–0.973; n = 4) | 825 (831) | 2 (2) |
| ZB06 | 6 / 0 / 0 / 0 | - | 1.000 (1.000–1.000; n = 6) | - | 1.000 (1.000–1.000; n = 6) | 862 (869) | 4 (4) |
| ZB07 | 2 / 3 / 1 / 0 | 0.921 (0.908–0.933; n = 3) | 0.965 (0.955–0.975; n = 2) | - | 0.910 (0.900–0.920; n = 6) | 503 (505) | 0 (0) |
| ZC01 | 0 / 2 / 2 / 0 | 1.001 (1.000–1.002; n = 2) | - | - | 0.970 (0.953–0.987; n = 4) | 832 (832) | 0 (0) |
| ZC02 | 3 / 0 / 0 / 1 | - | 1.000 (1.000–1.000; n = 3) | - | 1.000 (1.000–1.000; n = 4) | 832 (832) | 0 (0) |
| ZC03 | 0 / 3 / 0 / 1 | 1.001 (0.999–1.002; n = 3) | - | - | 0.950 (0.936–0.965; n = 4) | 783 (785) | 2 (2) |
| ZC04 | 0 / 2 / 0 / 1 | 1.000 (1.000–1.000; n = 2) | - | - | 0.965 (0.955–0.974; n = 3) | 827 (827) | 0 (0) |
| ZC05 | 3 / 0 / 0 / 0 | - | 1.000 (1.000–1.000; n = 3) | - | 1.000 (1.000–1.000; n = 3) | 159 (159) | 0 (0) |
| ZCURTAS | 25 / 4 / 13 / 0 | 1.003 (1.000–1.007; n = 4) | 1.000 (0.998–1.001; n = 25) | 1.000 (0.995–1.008; n = 42) | 0.986 (0.980–0.997; n = 42) | 273 (631) | 0 (0) |


## Critério 1 (F6) e decisão

Critério 1 (`M1_VAL5_ALVO_RESULTADO.md`): **atendido** em Z-B03 (1,118; meta 1,410; v0.52 1,169; custo 1,97 vez) e Z-B07
(0,925; meta 1,068; v0.52 1,017; custo 2,20 vezes). Nenhum passo de avaliação NaN (0 em 85 séries e nas 10 do critério 1).

**Decisão pela regra do plano: a v0.53 com a M1 rascunho 5 e a M2 candidata Q2 é confirmada na validação 5.** Primeira
confirmação em dados novos de M1 + M2 juntas, depois de 6 desenhos da M1 e 14 configurações da M2 (com a régua decidida e
emendada ao longo do desenvolvimento, sempre antes desta medição).

**Custo:** a v0.53 custa, por série, mediana de 2,13 vezes a v0.52 (1,39 a 3,24; Z-C04 3,23; Z-C01 2,98). Fica para o
pré-registro final (tensão com o pedido de <= 1,25 vez da nota de desenho; M5).
