# Diagnóstico E6 da M2 (oráculo de Jeffreys): plano, escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** `saida="switch_mono_jeffreys"` (lebre-research `4c8f102`): a candidata M (trocas só da
referência para a LEBRE, prioridade do artigo renormalizada) com a variância do ruído **integrada** pela prioridade de
Jeffreys (1/σ) em vez de estimada: verossimilhança marginal de cada hipótese ∝ C_h^(−n/2), C_h = erro quadrático
acumulado da hipótese em n rodadas. Sem escala estimada e sem parâmetro; invariante à escala dos dados (testado). Custo
O(t): **oráculo, não candidata**. Motivação: no E5 (escala atual = média exponencial), a evidência é achatada em
períodos agitados (Grand Isle, VB07); integrar a variância remove a escala estimada.

**Dados, régua:** as 43 famílias de desenvolvimento, régua por decidibilidade, sementes 20261024 e 20261025. Critério 5
(custo) não é considerado (O(t) por construção).

**Uso do resultado:** se atender aos critérios 1, 2, 4, 6 e 7 nas 43 famílias, desenhar uma aproximação barata e
medi-la contra o oráculo; se não, registrar e voltar à reflexão. Nada é selecionado aqui. Contagem: 11ª configuração.
