# Experimento E16 (desenvolvimento ampliado): M2 candidata Q e M1 rascunho 3, plano escrito e commitado antes de rodar

**Data:** 09/10/2026. **O quê:** a M2 candidata Q (`M2_CANDIDATA_Q.md`, lebre-research; protótipo `saida="prod_q"`) e a M1
rascunho 3 (`ALGORITHM_SPEC_DRAFT_M1_r3.md`; `precisao="r3"`), código do commit `db3bf1d` (a P e os rascunhos 1 e 2 da M1
continuam idênticos bit a bit). **Onde:** desenvolvimento ampliado: as 59 famílias do desenvolvimento e das validações 1 a
4 (todas já gastas) e as cinco famílias curtas (CURTAS, VCURTAS, WCURTAS, XCURTAS, YCURTAS). Não é evidência de seleção:
todos esses dados já orientaram desenhos. A confirmação será a validação 5, nova.

**Régua:** por decidibilidade (`M2_CANDIDATA_D.md`) **com o adendo de 09/10/2026**: série "referência melhor" cujo maior
passo isolado passa de 5% do erro quadrático da referência no período de avaliação fica "indecidível (choque)" no critério 1.
Sementes 20261042 (medição) e 20261043 (classificação). Blocos: 168 nas famílias horárias B, 12 nas C05, 20 nas demais;
curtas 24, 12 e 20.

**Critérios:**
1. **M2 Q sozinha** (`m2_e16.py q`): critérios 1, 2, 4, 5 (<= 150 FP por passo, máximo por família), 6 e 7, em todas as
   famílias.
2. **M1 r3 + M2 Q** (`m2_e16.py q_r3`): critérios 1, 2, 4, 6 e 7 em todas as famílias; custo reportado.
3. **F6** (`m2_e16_alvo.py`): em B03, B07, VB07 e XB07, custo da v0.53 <= 2,5 × v0.52 e erro <= 1,05 × o menor erro entre
   as variantes do E14 com custo <= o da v0.53.

**Regra:** Q fica como candidata da M2 se atender a 1; a M1 r3 fica se atender a 2 e 3. Se passarem, vão juntas para a
validação 5 (nova, congelada, usada uma vez). Se não, falhas declaradas, nada ajustado. Todas as famílias até o fim.
Contagem declarada: Q é a 13ª configuração da M2; o rascunho 3 é o 4º desenho da M1.
