# Candidata P da M2 na validação 3: resultado

Plano: `M2_VAL3_PLANO.md`. Protótipo: commit `6e43d9a`. B = 2000; sementes 20261028 (medição) e 20261029 (classificação).

Famílias não medidas: nenhuma.

| Critério | Falhas |
|---|---|
| 1 | - |
| 2 | - |
| 4 | - |
| 5 | - |
| 6 | - |
| 7 | - |

**P passa na validação 3.**

| Família | séries (v0.52 melhor / ref. melhor / indecidível) | 1: M2 ÷ ref nas "ref. melhor" | 2: M2 ÷ v0.52 nas "v0.52 melhor" | 7: M2 ÷ melhor | todas: M2 ÷ v0.52 | +custo | externas (v0.52) | estrutura |
|---|---|---|---|---|---|---|---|---|
| XB01 | 6 / 0 / 0 | - | 1.000 (1.000–1.000; n = 6) | - | 1.000 (1.000–1.000; n = 6) | 134.2 | 1 (1) | True |
| XB02 | 4 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 134.2 | 4 (4) | True |
| XB06 | 6 / 0 / 0 | - | 1.000 (1.000–1.000; n = 6) | - | 1.000 (1.000–1.000; n = 6) | 134.2 | 3 (3) | True |
| XB07 | 1 / 2 / 3 | 0.994 (0.992–0.996; n = 2) | 1.002 (0.991–1.011; n = 1) | - | 0.969 (0.964–0.974; n = 6) | 134.4 | 1 (1) | True |
| XC01 | 1 / 2 / 1 | 1.002 (1.000–1.004; n = 2) | 1.000 (1.000–1.000; n = 1) | - | 0.980 (0.963–0.992; n = 4) | 128.9 | 0 (0) | True |
| XC02 | 4 / 0 / 0 | - | 1.000 (1.000–1.000; n = 4) | - | 1.000 (1.000–1.000; n = 4) | 128.8 | 0 (0) | True |
| XC03 | 0 / 4 / 0 | 1.001 (1.000–1.002; n = 4) | - | - | 0.784 (0.698–0.942; n = 4) | 128.9 | 4 (4) | True |
| XC04 | 0 / 3 / 0 | 1.000 (1.000–1.000; n = 3) | - | - | 0.959 (0.949–0.968; n = 3) | 128.9 | 0 (0) | True |
| XC05 | 4 / 0 / 0 | - | 0.996 (0.991–0.999; n = 4) | - | 0.996 (0.991–0.999; n = 4) | 129.6 | 0 (0) | True |
| XCURTAS | 22 / 5 / 14 | 1.000 (1.000–1.001; n = 5) | 0.999 (0.993–1.008; n = 22) | 1.000 (0.995–1.005; n = 41) | 0.987 (0.981–0.995; n = 41) | 128.8 | 0 (0) | True |

## Séries indecidíveis (reportadas, sem aprovar nem reprovar)

| Família | Série | v0.52 ÷ ref (IC 95%) | M2 ÷ v0.52 | M2 ÷ ref |
|---|---|---|---|---|
| XB07 | 8447930_Woods Hole | 0.988 (0.970–1.005) | 1.000 | 0.988 |
| XB07 | 8638610_Sewells Point | 0.970 (0.932–1.012) | 1.001 | 0.971 |
| XB07 | 9410660_Los Angeles | 1.006 (0.992–1.022) | 0.974 | 0.981 |
| XC01 | rupia_sri_lanka | 1.000 (0.951–1.083) | 0.994 | 0.994 |
| XCURTAS | Conj. Floresta | 0.563 (0.395–1.032) | 1.000 | 0.563 |
| XCURTAS | NORDESTE_Recife_2010_2013 | 0.224 (0.122–1.001) | 1.000 | 0.224 |
| XCURTAS | 8461490_New London | 1.058 (0.970–1.141) | 0.945 | 1.000 |
| XCURTAS | 8447930_Woods Hole | 1.064 (0.955–1.117) | 0.940 | 1.000 |
| XCURTAS | 8638610_Sewells Point | 1.061 (0.979–1.185) | 0.943 | 1.000 |
| XCURTAS | 9410660_Los Angeles | 1.017 (0.929–1.133) | 0.973 | 0.990 |
| XCURTAS | 9440910_Toke Point | 0.979 (0.859–1.083) | 1.000 | 0.978 |
| XCURTAS | ringgit | 0.975 (0.923–1.065) | 1.002 | 0.977 |
| XCURTAS | dolar_taiwan | 0.984 (0.939–1.018) | 1.001 | 0.986 |
| XCURTAS | rupia_sri_lanka | 1.024 (0.991–1.055) | 0.980 | 1.004 |
| XCURTAS | rand | 1.039 (1.000–1.081) | 0.966 | 1.003 |
| XCURTAS | nivel_dolar_taiwan | 1.025 (0.984–1.058) | 0.976 | 1.000 |
| XCURTAS | nivel_rupia_sri_lanka | 1.018 (0.999–1.039) | 0.983 | 1.000 |
| XCURTAS | d_juro_3a | 1.026 (0.999–1.050) | 0.975 | 1.001 |

## Leitura

**P passa na validação 3**, em medição única com a régua por decidibilidade e o custo <= 150 FP por passo: nenhum
critério falha em nenhuma das 10 famílias; acréscimo de custo de 129 a 134 FP por passo. Destaques: X-C05 (análoga a C05)
0,996 contra a v0.52 (limite superior 0,999); X-CURTAS 1,000 / 0,999 / 1,000 nos critérios 1, 2 e 7; negativas 1,000 a
1,002; solar, eólica e carga 1,000. Nas séries indecidíveis (reportadas, sem aprovar nem reprovar), P fica no máximo 0,4%
acima do melhor entre v0.52 e referência. O commit registrado (`6e43d9a`) difere do commit do código da candidata
(`5c81d07`) só por documentação; `model053.py` e `agregacao.py` são os mesmos.
