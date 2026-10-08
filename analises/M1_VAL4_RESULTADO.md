# M1 rascunho 2 + M2 na validação 4 (critério 2): resultado

Plano: `M1_VAL4_PLANO.md`. Protótipo: commit `d3e098f`. B = 2000; sementes 20261040 (medição) e 20261041 (classificação).

Famílias não medidas: nenhuma.

| Critério | Falhas |
|---|---|
| 1 | YB07, YC01 |
| 2 | YB01 |
| 4 | - |
| 5 | - |
| 6 | - |
| 7 | - |

**M1 + M2 não atende a todos os critérios da M2 na validação 4.**

| Família | séries (v0.52 melhor / ref. melhor / indecidível) | 1: M2 ÷ ref nas "ref. melhor" | 2: M2 ÷ v0.52 nas "v0.52 melhor" | 7: M2 ÷ melhor | todas: M2 ÷ v0.52 | +custo | externas (v0.52) | estrutura |
|---|---|---|---|---|---|---|---|---|
| YB01 | 6 / 0 / 0 | - | 1.030 (1.024–1.038; n = 6) | - | 1.030 (1.024–1.038; n = 6) | 610.4 | 3 (3) | True |
| YB02 | 4 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 808.4 | 4 (4) | True |
| YB03 | 4 / 0 / 0 | - | 0.997 (0.995–0.998; n = 4) | - | 0.997 (0.995–0.998; n = 4) | 777.2 | 3 (3) | True |
| YB06 | 6 / 0 / 0 | - | 1.000 (1.000–1.000; n = 6) | - | 1.000 (1.000–1.000; n = 6) | 812.7 | 3 (3) | True |
| YB07 | 5 / 1 / 0 | 0.997 (0.978–1.015; n = 1) | 0.959 (0.951–0.966; n = 5) | - | 0.956 (0.949–0.962; n = 6) | 453.2 | 0 (0) | True |
| YC01 | 0 / 4 / 0 | 1.007 (1.000–1.016; n = 4) | - | - | 0.965 (0.955–0.974; n = 4) | 784.1 | 0 (0) | True |
| YC02 | 4 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 784.1 | 0 (0) | True |
| YC03 | 0 / 4 / 0 | 1.000 (0.999–1.001; n = 4) | - | - | 0.939 (0.919–0.960; n = 4) | 741.8 | 2 (2) | True |
| YC04 | 0 / 2 / 1 | 1.000 (1.000–1.000; n = 2) | - | - | 0.976 (0.967–0.986; n = 3) | 791.2 | 0 (0) | True |
| YC05 | 4 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 155.9 | 0 (0) | True |
| YCURTAS | 30 / 3 / 12 | 1.001 (1.001–1.005; n = 3) | 1.002 (1.000–1.005; n = 30) | 1.001 (0.995–1.006; n = 45) | 0.995 (0.989–1.001; n = 45) | 261.6 | 0 (0) | True |

## Séries indecidíveis (reportadas, sem aprovar nem reprovar)

| Família | Série | v0.52 ÷ ref (IC 95%) | M2 ÷ v0.52 | M2 ÷ ref |
|---|---|---|---|---|
| YC04 | d_juro_1a_1990 | 1.020 (0.998–1.040) | 0.981 | 1.000 |
| YCURTAS | 8410140_Eastport | 0.978 (0.803–1.221) | 0.862 | 0.843 |
| YCURTAS | 8413320_Bar Harbor | 1.082 (0.968–1.207) | 0.924 | 1.000 |
| YCURTAS | 8418150_Portland | 0.973 (0.919–1.064) | 0.987 | 0.961 |
| YCURTAS | iene_1990 | 1.017 (0.961–1.058) | 0.989 | 1.005 |
| YCURTAS | coroa_dinamarquesa_1990 | 1.017 (0.967–1.053) | 0.989 | 1.005 |
| YCURTAS | dolar_singapura_1990 | 0.949 (0.890–1.019) | 1.043 | 0.990 |
| YCURTAS | baht_1990 | 0.950 (0.709–1.017) | 1.018 | 0.967 |
| YCURTAS | abs_baht_1990 | 0.914 (0.489–1.258) | 1.045 | 0.955 |
| YCURTAS | nivel_iene_1990 | 1.016 (0.960–1.066) | 0.984 | 0.999 |
| YCURTAS | nivel_dolar_singapura_1990 | 1.003 (0.965–1.053) | 0.999 | 1.001 |
| YCURTAS | nivel_baht_1990 | 1.008 (0.997–1.023) | 0.993 | 1.000 |
| YCURTAS | d_juro_1a_1990 | 1.023 (0.997–1.052) | 0.978 | 1.000 |

## Critério 1 (F6) e decisão

Critério 1 (`M1_VAL4_ALVO_RESULTADO.md`): atendido pela regra (1,221 <= 1,466, custo 1,94 × v0.52), **mas sem
contribuição da M1**: a v0.52 sozinha dá 1,225 em Y-B03 e já atenderia; o peso final do especialista é ~0.

**Decisão pela regra do plano: a M1 rascunho 2 não é confirmada na validação 4** (critério 2 falha em Y-B01, Y-B07 e
Y-C01). Nada ajustado. Atribuição das falhas (M1 ou M2) só por diagnóstico descritivo separado.
