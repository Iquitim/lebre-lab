# Medição da M2, rascunho 5: resultado (parcial, interrompida)

Plano: `M2_DEV_R5_PLANO.md`. Protótipo: commit `244f7b3`. B = 2000, semente 20261013. Reprodução da v0.52 e conferência
do rascunho 2 (C05): diferença relativa 0.

Interrompida depois que a regra já estava decidida (C05 falhou o critério 2). **Resultado: Q não é escolhida.**

| Família | M2 ÷ ref (IC 95%) | M2 ÷ v0.52 (IC 95%) | M2 ÷ melhor (IC 95%) | peso L | +custo | estrutura idêntica |
|---|---|---|---|---|---|---|
| C05 | 0.427 (0.328–0.529) | 1.060 (1.007–1.132) | 1.060 (1.006–1.132) | 0.864 | 72.0 | True |
| CURTAS | 0.482 (0.462–0.512) | 0.973 (0.951–0.989) | 0.991 (0.970–1.006) | 0.662 | 70.6 | True |
| B01 | 0.231 (0.224–0.239) | 1.002 (1.001–1.002) | 1.002 (1.001–1.002) | 0.986 | 71.9 | True |
| C01 | 1.004 (1.000–1.008) | 0.940 (0.912–0.967) | 1.004 (1.000–1.008) | 0.222 | 69.4 | True |
| C02 | 0.601 (0.566–0.623) | 0.998 (0.998–0.999) | 0.998 (0.998–0.999) | 0.981 | 69.3 | True |
| C03 | 1.012 (1.001–1.019) | 0.947 (0.936–0.962) | 1.012 (1.001–1.019) | 0.291 | 69.4 | True |
| C04 | 1.006 (0.996–1.018) | 0.956 (0.929–0.983) | 1.006 (0.989–1.022) | 0.199 | 69.5 | True |

Não medidas: A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A12, B02, B03, B06, B07.

Falhas: critério 2 em C05 (limite superior 1,132 > 1,02); critério 1 em C03 (1,019) e C04 (1,018), > 1,01.
Passa: CURTAS (M2 ÷ melhor 0,991, limite superior 1,006) e B01 (1,002, limite superior 1,002: o esquecimento resolve a
série Arinos, que derrubou o rascunho 4).

## Diagnóstico (observação depois do resultado; nada foi alterado)

O rascunho 4 (sem compartilhamento) concentra os pesos e passa em C05 e nas negativas, mas demora a sair de um déficit
antigo (Arinos). O rascunho 5 (com compartilhamento α_t = 2/(t+1)) esquece o déficit e passa em Arinos e nas séries
curtas, mas não concentra: peso médio de L 0,86 em C05 e 0,20 a 0,29 nas negativas (onde deveria ficar perto de 0). Há
ainda um efeito de realimentação: como os pesos não concentram, o "mixability gap" cresce, o η do AdaHedge cai e os pesos
concentram ainda menos (o mesmo ciclo que de Rooij et al., 2014, seção 3, descrevem para o AdaHedge). É a troca conhecida
entre memória e adaptação.
