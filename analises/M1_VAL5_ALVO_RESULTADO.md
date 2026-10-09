# Validação 5, critério 1: F6 em Z-B03 e Z-B07 (fronteira recalculada)

Protótipo `bca5dac`. Plano `M1_VAL5_PLANO.md`.

| Família | custo v0.53 ÷ v0.52 | erro v0.53 | erro v0.52 | e* no custo da v0.53 (variante) | meta | atende |
|---|---|---|---|---|---|---|
| ZB03 | 1.97 | 1.118 | 1.169 | 1.343 (AR2+B3/8) | 1.410 | sim |
| ZB07 | 2.20 | 0.925 | 1.017 | 1.017 (AR2+0/1) | 1.068 | sim |

**Critério 1 (F6): atendido.**

Fronteira em ZB03:

| Variante | erro | FP |
|---|---|---|
| AR2+0/1 | 1.518 | 1192 |
| AR2+0/8 | 1.672 | 259 |
| AR2+B3/1 | 1.240 | 2082 |
| AR2+B3/8 | 1.343 | 318 |
| AR2+B-todas/1 | 1.040 | 17272 |
| AR2+B-todas/8 | 1.162 | 2339 |
| COMPLETO/1 | 1.000 | 52452 |
| COMPLETO/8 | 1.134 | 6719 |

Fronteira em ZB07:

| Variante | erro | FP |
|---|---|---|
| AR2+0/1 | 1.017 | 282 |
| AR2+0/8 | 1.049 | 72 |
| AR2+B3/1 | 0.990 | 2082 |
| AR2+B3/8 | 1.034 | 318 |
| AR2+B-todas/1 | 0.990 | 2082 |
| AR2+B-todas/8 | 1.034 | 318 |
| COMPLETO/1 | 1.000 | 5580 |
| COMPLETO/8 | 1.049 | 750 |

