# Medição da M2, rascunho 1: resultado

Plano: `M2_DEV_R1_PLANO.md`. Protótipo: commit `9bfdd0d`. B = 2000, semente 20261009.

Reprodução da v0.52 contra o registro do Lab: maior diferença relativa 0.0e+00. Conferência do rascunho 0 (C05, B06): maior diferença relativa 0.0e+00.

| Config | α_porta | 1 | 2 | 3 | 4 | 5 | 6 | M2 ÷ ref negativas (geo) | Famílias que falham |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 0.01 | sim | **não** | **não** | sim | sim | sim | 1.0000 | 2: C05, 3: C05 |
| A5 | 0.05 | sim | **não** | **não** | sim | sim | sim | 1.0000 | 2: C05, 3: C05 |

**Nenhuma configuração atende aos 6 critérios; nenhuma é escolhida.**

| Família | Config | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | trocas/2000 | séries c/ externa (v0.52) | +custo | estrutura idêntica |
|---|---|---|---|---|---|---|---|
| A01 | A1 | 0.302 (0.300–0.303) | 1.000 (1.000–1.000) | 0.10 | 30 (30) | 18.4 | True |
| A01 | A5 | 0.302 (0.301–0.303) | 1.000 (1.000–1.000) | 0.10 | 30 (30) | 18.4 | True |
| A02 | A1 | 0.825 (0.824–0.826) | 1.000 (1.000–1.000) | 0.10 | 0 (0) | 18.4 | True |
| A02 | A5 | 0.825 (0.824–0.826) | 1.000 (1.000–1.000) | 0.10 | 0 (0) | 18.4 | True |
| A03 | A1 | 0.280 (0.279–0.281) | 1.000 (1.000–1.000) | 0.10 | 30 (30) | 18.4 | True |
| A03 | A5 | 0.280 (0.279–0.281) | 1.000 (1.000–1.000) | 0.10 | 30 (30) | 18.4 | True |
| A04 | A1 | 0.542 (0.540–0.543) | 1.000 (1.000–1.000) | 0.10 | 10 (10) | 18.4 | True |
| A04 | A5 | 0.542 (0.540–0.543) | 1.000 (1.000–1.000) | 0.10 | 10 (10) | 18.4 | True |
| A05 | A1 | 0.308 (0.306–0.310) | 1.000 (1.000–1.000) | 0.07 | 20 (20) | 18.4 | True |
| A05 | A5 | 0.308 (0.306–0.310) | 1.000 (1.000–1.000) | 0.07 | 20 (20) | 18.4 | True |
| A06 | A1 | 0.314 (0.312–0.315) | 1.000 (1.000–1.000) | 0.07 | 20 (20) | 18.4 | True |
| A06 | A5 | 0.314 (0.312–0.315) | 1.000 (1.000–1.000) | 0.07 | 20 (20) | 18.4 | True |
| A07 | A1 | 0.362 (0.360–0.365) | 1.000 (1.000–1.000) | 0.07 | 20 (20) | 18.4 | True |
| A07 | A5 | 0.362 (0.360–0.365) | 1.000 (1.000–1.000) | 0.07 | 20 (20) | 18.4 | True |
| A08 | A1 | 0.320 (0.318–0.322) | 1.000 (1.000–1.000) | 0.10 | 20 (20) | 15.9 | True |
| A08 | A5 | 0.320 (0.318–0.322) | 1.000 (1.000–1.000) | 0.10 | 20 (20) | 15.9 | True |
| A09 | A1 | 0.488 (0.484–0.492) | 1.000 (1.000–1.000) | 0.10 | 20 (20) | 18.4 | True |
| A09 | A5 | 0.488 (0.484–0.492) | 1.000 (1.000–1.000) | 0.10 | 20 (20) | 18.4 | True |
| A10 | A1 | 0.375 (0.373–0.377) | 1.000 (1.000–1.000) | 0.10 | 20 (20) | 18.4 | True |
| A10 | A5 | 0.375 (0.373–0.377) | 1.000 (1.000–1.000) | 0.10 | 20 (20) | 18.4 | True |
| A11 | A1 | 0.311 (0.306–0.314) | 1.000 (1.000–1.000) | 0.10 | 40 (40) | 18.4 | True |
| A11 | A5 | 0.311 (0.306–0.314) | 1.000 (1.000–1.000) | 0.10 | 40 (40) | 18.4 | True |
| A12 | A1 | 0.293 (0.290–0.295) | 1.000 (1.000–1.000) | 0.01 | 1 (1) | 18.4 | True |
| A12 | A5 | 0.293 (0.290–0.295) | 1.000 (1.000–1.000) | 0.01 | 1 (1) | 18.4 | True |
| B01 | A1 | 0.231 (0.223–0.239) | 1.000 (1.000–1.001) | 0.11 | 4 (4) | 18.3 | True |
| B01 | A5 | 0.231 (0.223–0.239) | 1.000 (1.000–1.001) | 0.15 | 4 (4) | 18.3 | True |
| B02 | A1 | 0.036 (0.035–0.037) | 1.000 (1.000–1.000) | 0.06 | 4 (4) | 18.4 | True |
| B02 | A5 | 0.036 (0.034–0.037) | 1.000 (1.000–1.000) | 0.06 | 4 (4) | 18.4 | True |
| B03 | A1 | 0.113 (0.103–0.125) | 1.000 (1.000–1.000) | 0.21 | 4 (4) | 16.1 | True |
| B03 | A5 | 0.113 (0.103–0.124) | 1.000 (1.000–1.000) | 0.21 | 4 (4) | 16.1 | True |
| B06 | A1 | 0.117 (0.113–0.121) | 1.000 (1.000–1.000) | 0.11 | 4 (4) | 18.4 | True |
| B06 | A5 | 0.117 (0.112–0.121) | 1.000 (1.000–1.000) | 0.11 | 4 (4) | 18.4 | True |
| B07 | A1 | 0.933 (0.924–0.942) | 0.992 (0.983–1.001) | 0.03 | 1 (1) | 18.4 | True |
| B07 | A5 | 0.927 (0.917–0.936) | 0.985 (0.978–0.993) | 0.03 | 1 (1) | 18.4 | True |
| C01 | A1 | 1.000 (1.000–1.000) | 0.936 (0.905–0.966) | 0.00 | 0 (0) | 17.7 | True |
| C01 | A5 | 1.000 (1.000–1.000) | 0.936 (0.905–0.966) | 0.00 | 0 (0) | 17.7 | True |
| C02 | A1 | 0.602 (0.566–0.623) | 1.000 (1.000–1.000) | 0.48 | 0 (0) | 17.7 | True |
| C02 | A5 | 0.602 (0.566–0.623) | 1.000 (1.000–1.000) | 0.48 | 0 (0) | 17.7 | True |
| C03 | A1 | 1.000 (1.000–1.000) | 0.936 (0.919–0.961) | 0.00 | 4 (4) | 17.7 | True |
| C03 | A5 | 1.000 (1.000–1.000) | 0.936 (0.919–0.961) | 0.00 | 4 (4) | 17.7 | True |
| C04 | A1 | 1.000 (1.000–1.000) | 0.951 (0.912–0.986) | 0.00 | 0 (0) | 17.7 | True |
| C04 | A5 | 1.000 (1.000–1.000) | 0.951 (0.913–0.985) | 0.00 | 0 (0) | 17.7 | True |
| C05 | A1 | 0.833 (0.696–0.925) | 2.067 (1.485–2.987) | 5.56 | 0 (0) | 18.3 | True |
| C05 | A5 | 0.776 (0.612–0.875) | 1.925 (1.342–2.761) | 5.56 | 0 (0) | 18.3 | True |

## Leitura (escrita depois do cálculo)

- **Pela regra declarada, nenhuma configuração é escolhida:** as duas falham em C05, e só em C05 (critério 2: 2,07 vezes
  a v0.52 com α_porta = 0,01 e 1,92 com 0,05; critério 3: uma única troca em 360 passos equivale a 5,6 por 2.000).
- **Em C05 o rascunho 1 melhorou, mas não resolveu:** a porta passou a promover a LEBRE (passos 200 a 260 de 360), o que
  no rascunho 0 nunca acontecia; mesmo assim, ficar na referência sazonal até lá custa caro numa série curta. Conforme a
  especificação, C05 vira **limitação declarada**: em séries de poucas centenas de passos, a porta pode chegar tarde
  demais; nesse caso, `porta=False`. Nada foi ajustado para C05.
- **Nas outras 21 famílias, as duas configurações atendem aos 6 critérios** e são quase indistinguíveis: pior limite
  superior M2 ÷ v0.52 de 1,001; no máximo 0,48 troca por 2.000 passos; acréscimo de custo de no máximo 18,4 FP por passo;
  caminho estrutural idêntico ao da v0.52 em todas as séries; nas famílias negativas, a saída fica na referência
  (razão 1,000). A falha de custo de B06 no rascunho 0 desapareceu com o orçamento próprio da porta.
- **Diferença entre α_porta = 0,01 e 0,05:** só a velocidade da primeira promoção (0,05 promove mais cedo; ex.: carga em
  70 a 230 passos contra 180 a 330) e a garantia global (0,06 contra 0,10).
- **Reprodução:** v0.52 contra o registro do Lab e rascunho 0 contra os resultados anteriores, ambas com diferença 0.
