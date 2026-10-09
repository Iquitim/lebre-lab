# Validação 5 (M1 rascunho 5 + M2 candidata Q2): plano da medição, escrito e commitado antes de rodar

**Data:** 09/10/2026. **O quê:** a v0.53 com a M1 rascunho 5 (`ALGORITHM_SPEC_DRAFT_M1_r5.md`, `precisao="r5"`) e a M2
candidata Q2 (`M2_CANDIDATA_Q2.md`, `saida="prod_q2"`), código do commit `bca5dac` do lebre-research, rodado numa cópia fixa
(git worktree) desse commit. **Onde:** a validação 5 congelada (`VALIDACAO5_CONGELADA.md`, commit `11d1a84`), 43 séries em
10 famílias mais Z-CURTAS, usada **uma única vez**. Critérios os de `VALIDACAO5_PLANO.md`, inalterados.

1. **F6** (`m1_val5_alvo.py`): em Z-B03 e Z-B07, custo médio da v0.53 <= 2,5 × v0.52 e erro (geo ÷ comparador completo)
   <= 1,05 × o menor erro entre as 8 variantes do E14 recalculadas na família com custo <= o da v0.53. Sem sorteio.
2. **Critérios da M2** (`m1_val5.py`): régua por decidibilidade com o adendo 3 (limite do choque máx(5%, 5 × 2 ln(n)/n));
   critério 1 nas "referência melhor" (<= 1,01), 2 nas "v0.52 melhor" (<= 1,02), 4 em Z-C01 e Z-C04, 6 em todas, 7 em
   Z-CURTAS (<= 1,05); passo de avaliação com previsão não finita = falha. Sementes 20261051 (medição) e 20261052
   (classificação). Blocos: 168 nas Z-B, 20 em Z-C01 a Z-C04, 12 em Z-C05; nas curtas 24, 20 e 12.
3. **Custo** reportado.

**Regra:** a v0.53 (M1 r5 + M2 Q2) é confirmada se atender a 1 e 2. Se não, falhas declaradas, nada ajustado. Todas as
famílias até o fim. Contagem declarada: M1 rascunho 5 = 6º desenho da M1; Q2 = 14ª configuração da M2.
