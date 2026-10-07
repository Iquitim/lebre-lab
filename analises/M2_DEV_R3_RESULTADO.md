# Medição da M2, rascunho 3: resultado (parcial, interrompida)

Plano: `M2_DEV_R3_PLANO.md`. Protótipo: commit `bda07f4`. B = 2000, semente 20261011. Reprodução da v0.52 e conferência do
rascunho 2 (C05, config H): diferença relativa 0 onde medidas.

**A medição foi interrompida** depois que a configuração S já falhava em vários critérios: pela regra do plano (S só é
escolhida se atender a todos), as famílias restantes não podiam mudar o resultado. Famílias não medidas: listadas abaixo.

**Resultado: S não é escolhida.**

| Família | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | M2 ÷ melhor (IC 95%) | peso L | +custo | estrutura idêntica |
|---|---|---|---|---|---|---|
| C05 | 0.447 (0.318–0.570) | 1.108 (1.021–1.211) | 1.108 (1.024–1.215) | 0.916 | 55.1 | True |
| CURTAS | 0.542 (0.514–0.574) | 1.094 (1.057–1.120) | 1.115 (1.074–1.137) | 0.564 | 54.0 | True |
| B01 | 0.254 (0.245–0.263) | 1.102 (1.082–1.119) | 1.102 (1.082–1.120) | 0.958 | 55.0 | True |
| B02 | 0.041 (0.038–0.045) | 1.162 (1.081–1.245) | 1.162 (1.082–1.245) | 0.994 | 55.4 | True |
| C01 | 1.028 (1.003–1.060) | 0.962 (0.953–0.972) | 1.028 (1.003–1.058) | 0.089 | 53.1 | True |
| C02 | 0.638 (0.601–0.662) | 1.059 (1.036–1.083) | 1.059 (1.037–1.083) | 0.971 | 53.1 | True |
| C03 | 1.031 (1.002–1.050) | 0.965 (0.952–0.972) | 1.031 (1.002–1.050) | 0.101 | 53.1 | True |
| C04 | 0.999 (0.988–1.012) | 0.950 (0.913–0.980) | 1.000 (0.994–1.004) | 0.130 | 53.2 | True |

Não medidas: A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A12, B03, B06, B07.

Falhas: critério 2 (C05 1,108; B01 1,102; B02 1,162; C02 1,059, todos com limite superior > 1,02); critério 1 (C01, C03 e C04,
limite superior de M2 ÷ referência > 1,01, ver tabela); critério 7 (CURTAS, limite superior 1,137 contra o melhor).

## Diagnóstico (observação depois do resultado; nada foi alterado)

Com cada previsor avaliado pela perda logarítmica da sua própria gaussiana (σ² pela média exponencial dos próprios erros),
a vantagem por passo do melhor previsor é só ~½ ln(razão dos erros quadráticos médios), pequena diante do ruído de cada
passo; a média exponencial ainda aproxima as escalas (C05: σ² final 0,137 da referência contra 0,124 da LEBRE). O Fixed
Share, pronto para trocar a qualquer momento, segue sequências de sorte: em C05 o peso da LEBRE oscila entre 0,03 e 0,93.
É o custo conhecido do acompanhamento: com sinal fraco por passo, a disposição para trocar vira variância. O rascunho 3
melhora B02 curto (1,81 contra 2,40 do AdaHedge) mas piora quase todo o resto, inclusive C05, que o rascunho 2 resolvia.
