# Diagnóstico E17: M1 rascunho 3 (resultado)

Plano `E17_PLANO.md`. Só descrição. Dados: `e17_m1.json`.

| Série | L' ÷ v0.52 | especialista recortado ÷ v0.52 | sem recorte | s médio | passos no recorte |
|---|---|---|---|---|---|
| B01 Arinos | 1,421 | 1,435 | 1,580 | **0,987** | 6,6% |
| C05 ipca / inpc | 1,026 / 1,026 | 2,12 / 1,84 | 2,90 / 2,00 | 0,16 / 0,18 | |
| WC05 habitação, YC05 (4) | 0,994 a 1,023 | 1,33 a 3,24 | | 0,20 a 0,43 | |
| VB07 St. Petersburg | 0,980 | **0,747** | **0,626** | **0,036** | 0,6% |
| VB07 San Francisco | 1,047 | 1,061 | 1,085 | **0,982** | 3,1% |
| VB07 outras 4, B07 (6) | 0,85 a 0,97 | | | | < 1% |

**Leitura:**
- **H1 (recorte em VB07) não se sustenta como causa principal:** o recorte atua em menos de 1% dos passos nas marés. O
  problema é o **Prod**: em Arinos e San Francisco ele dá peso ~1 a um especialista **pior** que a v0.52; em St. Petersburg
  dá peso ~0 a um especialista **muito melhor** (0,63). É o risco declarado na especificação da Q: a normalização pelo
  maior erro já visto congela o Prod depois de um erro recorde (as perdas normalizadas ficam minúsculas e os pesos param
  onde estavam).
- **H2 (inflação mensal):** o especialista é muito pior (1,3 a 3,2 vezes) e entra tarde (17 a 74 passos de avaliação), mas
  o Prod começa com s = ½ (pesos iniciais iguais) e paga a entrada: 1-3% de piora, sempre no fim do período.
- **H3 (Arinos):** a piora cresce no meio do período (quintos 3 e 4), compatível com o congelamento depois da transição,
  não com um erro só na transição.
- Em St. Petersburg o recorte também custa (0,63 sem, 0,75 com).
