# Medição da M2, rascunho 4: resultado

Plano: `M2_DEV_R4_PLANO.md`. Protótipo: commit `432ef71`. B = 2000, semente 20261012.

Reprodução da v0.52 contra o registro do Lab: maior diferença relativa 0.0e+00. Conferência do rascunho 2 (C05, B06, config H): maior diferença relativa 0.0e+00.

| Config | Saída | 1 | 2 (C05 incl.) | 4 | 5 (<= 75) | 6 | 7 CURTAS | 5 com o limite antigo (<= 25) | M2 ÷ melhor, 23 famílias (geo) | Falhas |
|---|---|---|---|---|---|---|---|---|---|---|
| K | adahedge_recortada | sim | **não** | sim | sim | sim | sim | não | 1.0016 | 2: B01 |

**Nenhuma configuração atende aos critérios; nenhuma é escolhida.**

C05, K: M2 ÷ v0.52 = 1.001 (IC 95% 1.000–1.003); primeiro passo com peso de L > 0,9: [28, 56].

| Família | Config | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | M2 ÷ melhor (IC 95%) | peso L | |Δw|/passo | séries c/ externa (v0.52) | +custo | estrutura idêntica |
|---|---|---|---|---|---|---|---|---|---|
| A01 | K | 0.302 (0.301–0.303) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 30 (30) | 74.4 | True |
| A02 | K | 0.825 (0.824–0.827) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0003 | 0 (0) | 74.4 | True |
| A03 | K | 0.280 (0.279–0.281) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 30 (30) | 74.4 | True |
| A04 | K | 0.542 (0.540–0.543) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 10 (10) | 74.4 | True |
| A05 | K | 0.308 (0.306–0.310) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 20 (20) | 74.4 | True |
| A06 | K | 0.314 (0.312–0.315) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 20 (20) | 74.4 | True |
| A07 | K | 0.362 (0.360–0.365) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 20 (20) | 74.4 | True |
| A08 | K | 0.320 (0.318–0.322) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 20 (20) | 63.1 | True |
| A09 | K | 0.488 (0.484–0.492) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 20 (20) | 74.4 | True |
| A10 | K | 0.375 (0.373–0.377) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0002 | 20 (20) | 74.4 | True |
| A11 | K | 0.311 (0.306–0.314) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 40 (40) | 74.4 | True |
| A12 | K | 0.293 (0.290–0.295) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0000 | 1 (1) | 74.4 | True |
| B01 | K | 0.236 (0.228–0.245) | 1.024 (1.009–1.043) | 1.024 (1.009–1.043) | 0.961 | 0.0002 | 4 (4) | 73.9 | True |
| B02 | K | 0.036 (0.035–0.037) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 4 (4) | 74.4 | True |
| B03 | K | 0.113 (0.103–0.125) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0005 | 4 (4) | 64.1 | True |
| B06 | K | 0.117 (0.112–0.121) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0001 | 4 (4) | 74.2 | True |
| B07 | K | 0.922 (0.913–0.931) | 0.980 (0.973–0.986) | 1.000 (0.998–1.002) | 0.468 | 0.0004 | 1 (1) | 74.4 | True |
| C01 | K | 1.000 (0.999–1.000) | 0.936 (0.903–0.966) | 1.000 (0.999–1.000) | 0.010 | 0.0009 | 0 (0) | 71.3 | True |
| C02 | K | 0.602 (0.565–0.623) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0.0006 | 0 (0) | 71.3 | True |
| C03 | K | 1.000 (1.000–1.001) | 0.936 (0.919–0.961) | 1.000 (1.000–1.001) | 0.011 | 0.0006 | 4 (4) | 71.3 | True |
| C04 | K | 1.000 (1.000–1.000) | 0.951 (0.910–0.986) | 1.001 (0.986–1.013) | 0.000 | 0.0003 | 0 (0) | 71.4 | True |
| C05 | K | 0.403 (0.299–0.515) | 1.001 (1.000–1.003) | 1.001 (1.000–1.003) | 0.999 | 0.0071 | 0 (0) | 74.0 | True |
| CURTAS | K | 0.492 (0.470–0.526) | 0.994 (0.975–1.008) | 1.013 (0.993–1.023) | 0.634 | 0.0075 | 0 (0) | 72.6 | True |

## CURTAS por origem (média geométrica de M2 ÷ melhor por série)

| Origem | K | melhor (v0.52 / ref) |
|---|---|---|
| B01 | 1.158 | 5 / 0 |
| B02 | 0.975 | 4 / 0 |
| B03 | 0.955 | 4 / 0 |
| B06 | 1.000 | 6 / 0 |
| B07 | 1.012 | 2 / 4 |
| C01 | 1.000 | 0 / 4 |
| C02 | 1.000 | 4 / 0 |
| C03 | 1.000 | 0 / 4 |
| C04 | 1.000 | 0 / 3 |
| C05 | 1.001 | 2 / 0 |

## Diagnóstico da falha em B01 (observação depois do resultado; nada foi alterado)

A falha vem de uma série, "Conj. Arinos 2 500 kV" (M2 ÷ v0.52 = 1,154; as outras cinco ficam em 1,000). A usina começa a
gerar no passo 720 e a LEBRE leva milhares de passos para aprendê-la. Com a perda recortada, cada erro grande da
referência conta no máximo 1, e a vantagem por passo da LEBRE fica pequena (~0,035 entre os passos 3.600 e 6.000),
embora o MSE da v0.52 na série seja 4,4 vezes menor. O déficit da fase de aprendizado só é recuperado por volta do passo
6.500; até lá a saída fica na referência. Mesma raiz das falhas anteriores: os pesos dependem de todo o histórico. O
recorte corrigiu B02 curto (déficit limitado a 1 por passo) mas enfraqueceu a discriminação onde os erros da referência
são grandes.
