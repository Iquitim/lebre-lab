# Experimento E18b (desenvolvimento ampliado): M2 candidata Q2 e M1 rascunho 4, plano escrito e commitado antes de rodar

**Data:** 09/10/2026. **O quê:** a M2 candidata Q2 (`M2_CANDIDATA_Q2.md`, lebre-research; `saida="prod_q2"`) e a M1
rascunho 4 (`ALGORITHM_SPEC_DRAFT_M1_r4.md`; `precisao="r4"`), código do commit `fc71880` (inclui a correção do NaN do
subagregador M; P, Q e os rascunhos 1 a 3 da M1 idênticos bit a bit fora do caso corrigido). **Onde:** o mesmo
desenvolvimento ampliado do E16 (64 famílias). Não é evidência de seleção; a confirmação será a validação 5.

**Régua:** por decidibilidade com os adendos 1 e 2 de 09/10/2026 (choque > 5% → indecidível nos critérios 1 e 2). Sementes
20261045 (medição) e 20261046 (classificação). Blocos como no E16. **Auditoria permanente:** passos de avaliação com
previsão não finita contados; qualquer um é falha.

**Critérios:**
1. **Q2 sozinha** (`m2_e18b.py q2`): critérios 1, 2, 4, 5 (<= 150 FP), 6 e 7 em todas as famílias.
2. **M1 r4 + Q2** (`m2_e18b.py q2_r4`): critérios 1, 2, 4, 6 e 7 em todas as famílias; custo reportado.
3. **F6** (`m2_e18b_alvo.py`): em B03, B07, VB07 e XB07, custo da v0.53 <= 2,5 × v0.52 e erro <= 1,05 × o menor erro entre
   as variantes do E14 com custo <= o da v0.53.

**Regras:** entre Q e Q2, a de `M2_CANDIDATA_Q2.md` (se as duas atenderem, fica a Q2). A M1 r4 fica se atender a 2 e 3.
O que ficar vai para a validação 5. Falhas declaradas, nada ajustado. Contagem: Q2 é a 14ª configuração da M2; o rascunho
4 é o 5º desenho da M1.
