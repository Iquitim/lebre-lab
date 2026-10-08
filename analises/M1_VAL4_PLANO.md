# M1 rascunho 2 + M2 na validação 4: plano, escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** a M1 rascunho 2 (`ALGORITHM_SPEC_DRAFT_M1_r2.md`, lebre-research; protótipo
`precisao="r2"`, código do commit `212c95f`, sem mudanças no protótipo desde então) com a M2 candidata P
(`saida="prod"`). **Onde:** a validação 4 congelada (`VALIDACAO4_CONGELADA.md`, commit `ef6f8a7`), 43 séries em 10
famílias mais Y-CURTAS, usada **uma única vez**. Critérios os de `VALIDACAO4_PLANO.md` (commit `6e923a5`), inalterados.

1. **F6 em Y-B03 (fronteira):** `m1_val4_alvo.py`. Custo médio da v0.53 <= 2,5 × o da v0.52 (mesma execução) e erro
   (média geométrica das 4 séries ÷ comparador linear online completo) <= 1,05 × o menor erro entre as 8 variantes do E10
   recalculadas em Y-B03 (AR2+0, AR2+B3, AR2+B-todas, completo; a cada passo e a cada 8; classes e fórmula de custo de
   `diagnosticos/f6_e10.py`, com o d de Y-B03 = 10) com custo <= o da v0.53. Sem sorteio.
2. **Critérios da M2** (régua por decidibilidade, `M2_CANDIDATA_D.md`) com M1 + M2 em todas as famílias Y, Y-C05 incluída:
   `m1_val4.py`, sementes 20261040 (medição) e 20261041 (classificação). Critério 1 nas "referência melhor" (<= 1,01),
   2 nas "v0.52 melhor" (<= 1,02), 4 em Y-C01 e Y-C04, 6 em todas, 7 em Y-CURTAS (<= 1,05). Blocos: 168 nas Y-B, 20 nas
   Y-C01 a Y-C04, 12 em Y-C05; nas curtas 24, 20 e 12.
3. **Custo** reportado (acréscimo por passo sobre a v0.52, por família); o teto da v0.53 como um todo é decidido no
   pré-registro final.

**Regra:** a M1 é confirmada se atender a 1 e 2. Se não, as falhas são declaradas e nada é ajustado. Todas as famílias
são medidas até o fim. Contagem declarada: a M1 rascunho 2 é o 3º desenho da M1 (rascunhos 0, 1, 2).
