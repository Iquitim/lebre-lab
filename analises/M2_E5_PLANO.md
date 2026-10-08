# Diagnóstico E5 da M2 (oráculo): plano, escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** `saida="switch_mono_exato"` (lebre-research `85da1ff`): a posterior da candidata M
calculada a cada passo com a escala comum atual aplicada a **toda** a evidência acumulada (verossimilhança gaussiana de
variância σ̂² sobre todos os dados), em vez do produto de verossimilhanças de um passo com escalas diferentes. Custo O(t)
por passo: **não é candidata**, é um oráculo para saber se a correção da distorção de escala do início (E4) resolve o
critério 1 sem perder o critério 2. O critério 5 (custo) falha por construção e não é considerado.

**Dados, régua:** as 43 famílias de desenvolvimento, régua por decidibilidade, sementes 20261022 e 20261023.

**Uso do resultado:** se o oráculo atender aos critérios 1, 2, 4, 6 e 7 nas 43 famílias, o próximo passo é desenhar uma
aproximação barata (dentro do custo) e medi-la; se não, a ideia é descartada. Nada é selecionado aqui.
