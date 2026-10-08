# Experimento E3 da M2 (desenvolvimento): candidata S, plano escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** candidata S (`M2_CANDIDATA_S.md`, lebre-research; protótipo `saida="switch"`, commit
`462faee`): switch distribution de van Erven et al. (2012) com a prioridade (11) do artigo, sobre gaussianas de variância
comum, comparando só com a referência definida. Oitava configuração da M2.

**Natureza:** desenvolvimento. Dados: as 23 famílias do banco de desenvolvimento, as 10 da validação 1 e as 10 da
validação 2 (todas já gastas para seleção). **Nenhum resultado daqui é evidência de seleção.**

**Régua:** por decidibilidade (`M2_CANDIDATA_D.md`): classificação de cada série por v0.52 ÷ referência (semente
20261019); critério 1 nas "referência melhor" (<= 1,01), 2 nas "v0.52 melhor" (<= 1,02), 4 em A02, C01, C04, VC01, VC04,
W-C01, W-C04, 5 (<= 75 FP por passo) e 6 em todas, 7 nas três famílias curtas (<= 1,05). Medição com semente 20261018.

**Regra (fixada antes):** se S atender a todos os critérios nas 43 famílias, S vai à **validação 3** (nova, regras antes
do download, congelada, usada uma vez). Se não, as falhas orientam o próximo passo; nada é selecionado.
