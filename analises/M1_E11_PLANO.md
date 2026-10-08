# Experimento E11 (desenvolvimento): M1 rascunho 1 com a M2, plano escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** M1 rascunho 1 (`ALGORITHM_SPEC_DRAFT_M1_r1.md`, lebre-research; protótipo
`precisao="r1"`, commit `bec5307`): especialista RLS com alvo defasado e bandas de defasagem da v0.52 das até 8 entradas
mais correlacionadas, atualizado a cada 8 passos, combinado com a v0.52 pelo (A,B)-Prod anytime; a M2 (candidata P)
combina a referência com esse L'.

**Natureza:** desenvolvimento; a avaliação final é na reserva.

**Critérios (da especificação; fixados antes):**
1. **F6 (B03), fronteira:** custo médio da v0.53 em B03 <= 2,5 vezes o da v0.52 (mesma execução) e erro (média
   geométrica ÷ comparador linear completo) <= 1,05 × o menor erro entre as 8 variantes do E10 com custo <= o da v0.53.
   Script `m1_e11_alvo.py` (semente 20261033).
2. B01 e B02: limite superior do IC 95% de (M1 + M2) ÷ (M2 sozinha) <= 1,02. Mesmo script.
3. Critérios da M2 (régua por decidibilidade) nas 43 famílias com M1 ligada, **C05 incluída**. Script `m1_e11.py`
   (sementes 20261034 e 20261035). Custo reportado (o teto da v0.53 como um todo é decidido no pré-registro final).

**Regra:** a M1 fica se atender a 1, 2 e 3. Se não, falhas declaradas e nada ajustado. Contagem: segundo desenho da M1.
