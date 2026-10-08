# Experimento E12 (desenvolvimento): M1 rascunho 2 com a M2, plano escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** M1 rascunho 2 (`ALGORITHM_SPEC_DRAFT_M1_r2.md`, lebre-research; protótipo
`precisao="r2"`, commit `212c95f`): o especialista de defasagens conjuntas do rascunho 1 com m = mín(d, 5) (do teto de
custo total) e previsão recortada para L ± CLIP_K × σ̂_L; proteção numérica na M2 (sem efeito com valores finitos: a
candidata P sem M1 é idêntica bit a bit ao commit validado `5c81d07`). Terceiro desenho da M1.

**Critérios (os de `M1_E11_PLANO.md`, inalterados):**
1. F6 em B03: custo médio da v0.53 <= 2,5 vezes o da v0.52 e erro (geo ÷ comparador completo) <= 1,05 × o menor erro
   entre as 8 variantes do E10 com custo <= o da v0.53. Script `m1_e12_alvo.py` (semente 20261036).
2. B01 e B02: limite superior do IC 95% de (M1 + M2) ÷ (M2 sozinha) <= 1,02. Mesmo script.
3. Critérios da M2 (régua por decidibilidade) nas 43 famílias com M1 ligada, **C05 incluída**. Script `m1_e12.py`
   (sementes 20261037 e 20261038). Custo reportado.

**Regra:** a M1 fica se atender a 1, 2 e 3. Se não, falhas declaradas, nada ajustado. Todas as famílias até o fim.
