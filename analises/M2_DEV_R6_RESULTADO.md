# Medição da M2, rascunho 6: resultado (desenvolvimento e validação)

Plano: `M2_DEV_R6_PLANO.md`. Protótipo: commit `6a007d2`. B = 2000, semente 20261014.

Reprodução da v0.52 contra o registro do Lab (desenvolvimento): maior diferença relativa 0.0e+00. Conferência do rascunho 2 (C05, B06): [0.0, 0.0].

Famílias não medidas: nenhuma.

| Base | 1 | 2 | 4 | 5 (<= 75) | 6 | 7 | Falhas |
|---|---|---|---|---|---|---|---|
| desenvolvimento | **não** | sim | sim | sim | sim | sim | 1: C04 |
| validação | sim | **não** | sim | sim | sim | sim | 2: VC05 |

**R6 não é escolhida** (falha em algum critério, ou medição incompleta).

| Família | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | M2 ÷ melhor (IC 95%) | peso L | séries c/ externa (v0.52) | +custo | estrutura idêntica |
|---|---|---|---|---|---|---|---|
| A01 | 0.302 (0.301–0.303) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 30 (30) | 72.4 | True |
| A02 | 0.825 (0.824–0.827) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0 (0) | 72.4 | True |
| A03 | 0.280 (0.279–0.281) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 30 (30) | 72.4 | True |
| A04 | 0.542 (0.540–0.543) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 10 (10) | 72.4 | True |
| A05 | 0.308 (0.306–0.310) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 20 (20) | 72.4 | True |
| A06 | 0.314 (0.312–0.315) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 20 (20) | 72.4 | True |
| A07 | 0.362 (0.360–0.365) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 20 (20) | 72.4 | True |
| A08 | 0.320 (0.318–0.322) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 20 (20) | 61.4 | True |
| A09 | 0.488 (0.484–0.492) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 20 (20) | 72.4 | True |
| A10 | 0.375 (0.373–0.377) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 20 (20) | 72.4 | True |
| A11 | 0.311 (0.306–0.314) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 40 (40) | 72.4 | True |
| A12 | 0.293 (0.290–0.295) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 1 (1) | 72.4 | True |
| B01 | 0.231 (0.223–0.239) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 0.996 | 4 (4) | 71.9 | True |
| B02 | 0.036 (0.035–0.037) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 4 (4) | 72.4 | True |
| B03 | 0.113 (0.103–0.124) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 4 (4) | 62.4 | True |
| B06 | 0.117 (0.113–0.121) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 4 (4) | 72.2 | True |
| B07 | 0.920 (0.910–0.929) | 0.978 (0.971–0.985) | 0.998 (0.996–1.000) | 0.493 | 1 (1) | 72.4 | True |
| C01 | 1.000 (0.999–1.000) | 0.936 (0.903–0.966) | 1.000 (0.999–1.000) | 0.019 | 0 (0) | 69.4 | True |
| C02 | 0.602 (0.567–0.623) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0 (0) | 69.3 | True |
| C03 | 1.000 (0.999–1.001) | 0.936 (0.919–0.960) | 1.000 (0.999–1.001) | 0.033 | 4 (4) | 69.4 | True |
| C04 | 1.006 (0.999–1.014) | 0.956 (0.924–0.986) | 1.006 (0.989–1.021) | 0.074 | 0 (0) | 69.5 | True |
| C05 | 0.403 (0.299–0.506) | 1.001 (1.000–1.002) | 1.001 (1.000–1.002) | 0.998 | 0 (0) | 72.0 | True |
| CURTAS | 0.491 (0.469–0.526) | 0.991 (0.977–1.002) | 1.009 (0.994–1.018) | 0.654 | 0 (0) | 70.6 | True |
| VB01 | 0.232 (0.223–0.240) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 3 (3) | 71.9 | True |
| VB02 | 0.040 (0.036–0.043) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 4 (4) | 72.4 | True |
| VB06 | 0.121 (0.116–0.125) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 4 (4) | 72.4 | True |
| VB07 | 0.948 (0.887–1.008) | 0.977 (0.968–0.986) | 1.041 (0.976–1.103) | 0.789 | 2 (2) | 70.8 | True |
| VC01 | 1.001 (0.996–1.007) | 0.957 (0.946–0.968) | 1.001 (0.996–1.006) | 0.099 | 0 (0) | 67.6 | True |
| VC02 | 0.584 (0.559–0.607) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 | 0 (0) | 67.6 | True |
| VC03 | 1.001 (0.997–1.005) | 0.945 (0.931–0.960) | 1.001 (0.996–1.005) | 0.066 | 3 (3) | 67.6 | True |
| VC04 | 1.000 (1.000–1.000) | 0.955 (0.937–0.967) | 1.000 (1.000–1.000) | 0.007 | 0 (0) | 69.4 | True |
| VC05 | 0.543 (0.474–0.622) | 0.997 (0.938–1.063) | 0.997 (0.939–1.063) | 0.775 | 0 (0) | 71.9 | True |
| VCURTAS | 0.492 (0.473–0.522) | 0.998 (0.977–1.020) | 1.014 (0.992–1.034) | 0.603 | 0 (0) | 70.5 | True |

## Leitura das duas falhas (observação depois do resultado; nada foi alterado)

- **C04 (critério 1, limite superior 1,0145 > 1,01):** vem de uma série, d_juro_2a (M2 ÷ referência 1,0175, peso médio de
  L 0,22); nas outras duas o peso de L fica em 0 e a razão em 1,000. O compartilhamento restante, embora pequeno, ainda
  deixa a LEBRE levar peso onde a referência é melhor.
- **VC05 (critério 2, limite superior 1,063 > 1,02):** nenhuma série fica pior que a v0.52 no ponto (1,000; 1,000; 0,990;
  1,000). A falha vem da incerteza em IPCA serviços, onde os pesos ficam na referência (peso de L 0,11), a v0.52 é só 7%
  melhor que ela, e 288 meses avaliados (24 blocos de 12) não bastam para garantir a margem de 2%. Observação de método,
  não aplicada: em séries curtas, o critério 2 só aprova, na prática, uma saída idêntica à da v0.52.

## Conclusão, pela regra do plano

O rascunho 6 não vai à reserva. A M2 não é resolvida na v0.53 por este caminho, e não há rascunho 7 neste banco. Mapa
das seis tentativas: a porta (rascunhos 0 e 1) falha em C05; AdaHedge com perda quadrática (2) falha nas séries curtas;
Fixed Share sobre perda logarítmica (3) falha em quase tudo; AdaHedge com perda recortada (4) falha em B01 (Arinos);
compartilhamento com troca 1/t (5) falha em C05 e nas negativas; troca 1/t² (6) falha em C04 e VC05 por pouco.
