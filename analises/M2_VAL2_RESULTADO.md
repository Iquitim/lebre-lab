# Candidata D da M2 na validação 2: resultado

Plano: `M2_VAL2_PLANO.md`. Protótipo: commit `442db78`. B = 2000; sementes 20261016 (medição) e 20261017 (classificação).

Famílias não medidas: nenhuma.

| Critério | Falhas |
|---|---|
| 1 | - |
| 2 | WB01 |
| 4 | - |
| 5 | - |
| 6 | - |
| 7 | - |

**D não passa na validação 2.**

| Família | séries (v0.52 melhor / ref. melhor / indecidível) | 1: M2 ÷ ref nas "ref. melhor" | 2: M2 ÷ v0.52 nas "v0.52 melhor" | 7: M2 ÷ melhor | todas: M2 ÷ v0.52 | +custo | externas (v0.52) | estrutura |
|---|---|---|---|---|---|---|---|---|
| WB01 | 6 / 0 / 0 | - | 1.065 (1.033–1.099; n = 6) | - | 1.065 (1.033–1.099; n = 6) | 65.5 | 2 (2) | True |
| WB02 | 4 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 66.3 | 4 (4) | True |
| WB06 | 6 / 0 / 0 | - | 1.000 (1.000–1.000; n = 6) | - | 1.000 (1.000–1.000; n = 6) | 66.3 | 4 (4) | True |
| WB07 | 4 / 2 / 0 | 1.000 (1.000–1.000; n = 2) | 1.001 (0.998–1.005; n = 4) | - | 0.984 (0.978–0.988; n = 6) | 66.4 | 1 (1) | True |
| WC01 | 0 / 4 / 0 | 1.000 (1.000–1.001; n = 4) | - | - | 0.977 (0.969–0.984; n = 4) | 63.7 | 0 (0) | True |
| WC02 | 4 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 63.7 | 0 (0) | True |
| WC03 | 0 / 4 / 0 | 1.000 (1.000–1.000; n = 4) | - | - | 0.964 (0.956–0.973; n = 4) | 63.7 | 3 (3) | True |
| WC04 | 0 / 2 / 1 | 1.000 (1.000–1.000; n = 2) | - | - | 0.974 (0.965–0.982; n = 3) | 63.7 | 0 (0) | True |
| WC05 | 3 / 0 / 0 | - | 1.004 (0.997–1.019; n = 3) | - | 1.004 (0.997–1.019; n = 3) | 64.3 | 0 (0) | True |
| WCURTAS | 23 / 4 / 12 | 1.000 (1.000–1.001; n = 4) | 1.000 (0.994–1.008; n = 23) | 1.000 (0.996–1.005; n = 39) | 0.980 (0.974–0.993; n = 39) | 63.9 | 0 (0) | True |

## Séries indecidíveis (reportadas, sem aprovar nem reprovar)

| Família | Série | v0.52 ÷ ref (IC 95%) | M2 ÷ v0.52 | M2 ÷ ref |
|---|---|---|---|---|
| WC04 | d_juro_1a | 1.011 (0.977–1.039) | 0.990 | 1.001 |
| WCURTAS | 8454000_Providence | 1.157 (0.974–1.204) | 0.864 | 1.000 |
| WCURTAS | 8452660_Newport | 1.023 (0.975–1.104) | 0.977 | 1.000 |
| WCURTAS | 8545240_Philadelphia | 1.051 (0.979–1.115) | 0.951 | 1.000 |
| WCURTAS | 9418767_North Spit | 1.240 (0.929–1.539) | 0.806 | 1.000 |
| WCURTAS | rupia | 1.014 (0.980–1.048) | 0.987 | 1.001 |
| WCURTAS | baht | 0.990 (0.914–1.047) | 1.004 | 0.994 |
| WCURTAS | coroa_dinamarquesa | 1.007 (0.970–1.045) | 0.992 | 0.999 |
| WCURTAS | nivel_rupia | 1.017 (0.999–1.040) | 0.983 | 1.000 |
| WCURTAS | nivel_dolar_singapura | 1.021 (0.985–1.048) | 0.980 | 1.000 |
| WCURTAS | nivel_baht | 0.998 (0.911–1.079) | 1.002 | 1.000 |
| WCURTAS | nivel_coroa_dinamarquesa | 1.026 (0.972–1.085) | 0.975 | 1.000 |
| WCURTAS | d_juro_5a | 1.024 (0.999–1.050) | 0.976 | 1.000 |

## Leitura da falha (observação depois do resultado; nada foi alterado)

A única falha é o critério 2 em W-B01, por uma série: **Abaiara 230 kV** (M2 ÷ v0.52 = 1,460, IC 95% 1,22–1,76; as
outras cinco usinas ficam em 1,000). A usina começa a gerar no passo 720 (como Arinos no desenvolvimento). Nos ~800
passos seguintes a LEBRE ainda aprende a usina e erra muito mais que a referência (MSE 4.576 contra 754 entre os passos
700 e 1.500); depois passa a ser 2 a 5 vezes melhor. Com o erro quadrático acumulado, o déficit dessa fase só é
recuperado por volta do passo 6.000, e a janela de avaliação começa em 3.509: ~2.500 passos de avaliação ficam na
referência. É a dificuldade D1 (a LEBRE aprende) de `REFLEXAO_M2.md`, que a candidata D não resolve quando a fase de
aprendizado é longa. Todas as outras famílias passaram, inclusive W-C05 (análoga a C05) e W-CURTAS.
