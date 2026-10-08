# Validação 4, critério 1: F6 em Y-B03 (fronteira recalculada)

Protótipo `d3e098f`. Plano `M1_VAL4_PLANO.md`.

Custo da v0.53 em Y-B03 1607 FP por passo (1.94 × v0.52, teto 2,5). Melhor variante com custo <= esse: erro 1.397; meta 1.466; obtido 1.221 (v0.52: 1.225).

**Critério 1: atendido.**

| Variante | erro (geo ÷ completo) | FP por passo |
|---|---|---|
| AR2+0/1 | 1.506 | 1192 |
| AR2+0/8 | 1.719 | 259 |
| AR2+B3/1 | 1.230 | 2082 |
| AR2+B3/8 | 1.397 | 318 |
| AR2+B-todas/1 | 1.044 | 17272 |
| AR2+B-todas/8 | 1.228 | 2339 |
| COMPLETO/1 | 1.000 | 52452 |
| COMPLETO/8 | 1.175 | 6719 |

| Série | v0.53 ÷ linear | v0.52 ÷ linear | custo v0.53 | custo v0.52 |
|---|---|---|---|---|
| Aotizhongxin_PM2.5 | 1.259 | 1.261 | 1619 | 832 |
| Aotizhongxin_NO2 | 1.321 | 1.336 | 1668 | 884 |
| Aotizhongxin_CO | 1.145 | 1.145 | 1570 | 800 |
| Aotizhongxin_O3 | 1.166 | 1.168 | 1572 | 803 |
