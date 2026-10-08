# Experimento E8 (desenvolvimento): M1 enxuta com a M2, plano escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** M1 (`ALGORITHM_SPEC_DRAFT_M1.md`, lebre-research; protótipo `precisao=True`, commit
`af36e4a`): especialista de precisão (RLS sobre as 3 entradas de maior correlação, atualizado a cada 8 passos), combinado
com a v0.52 pelo (A,B)-Prod anytime; a M2 (candidata P, congelada) combina a referência com esse L'.

**Natureza:** desenvolvimento (banco do Lab e validações 1-3, todas já gastas para seleção). Nenhum resultado daqui é
evidência final; a avaliação final da v0.53 completa é na reserva.

**Critérios (da especificação, seção 5):**
1. B03: MSE de M1 + M2 no máximo 1,05 vez o do linear online (média geométrica das 4 séries). Script `m1_e8_alvo.py`.
2. B01 e B02: limite superior do IC 95% de (M1 + M2) ÷ (M2 sozinha) <= 1,02 (bootstrap de blocos pareado, B = 2000,
   blocos 168, semente 20261032). Script `m1_e8_alvo.py`.
3. Critérios da M2 (régua por decidibilidade) nas 43 famílias com M1 ligada; custo de M1 + M2 <= 150 + 70 + d FP por
   passo (d médio da família). Script `m1_e8.py`, sementes 20261030 e 20261031.
4. Custo da M1 reportado.

**Regra:** a M1 fica se atender a 1, 2 e 3. Se não, as falhas orientam o próximo passo; nada é ajustado para passar.
