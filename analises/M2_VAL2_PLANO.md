# Candidata D da M2 na validação 2: plano, escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** a candidata D congelada em `M2_CANDIDATA_D.md` (lebre-research `442db78`; protótipo
`saida="adahedge_ref_definida"`, código do commit `a0e20e1`; o script registra o commit atual do repositório e o hash
de `model053.py`, que não mudou desde `a0e20e1`). **Onde:** a validação 2 congelada (`VALIDACAO2_CONGELADA.md`, commit
`70349ca`), 40 séries em 9 famílias mais W-CURTAS, usada **uma única vez**.

**Régua:** a de `M2_CANDIDATA_D.md`, por decidibilidade. Classificação de cada série pela razão v0.52 ÷ referência com
bootstrap de blocos pareado (B = 2000, semente 20261017; blocos 168 horárias, 20 dias úteis, 12 mensais; em W-CURTAS 24,
20, 12). Critério 1 nas séries "referência melhor" (limite superior de M2 ÷ referência <= 1,01), critério 2 nas "v0.52
melhor" (limite superior de M2 ÷ v0.52 <= 1,02), por família; 4 em W-C01 e W-C04; 5 (<= 75 FP por passo) e 6 em todas;
7 em W-CURTAS (limite superior de M2 ÷ melhor <= 1,05). Medição com semente 20261016. Indecidíveis reportadas sem
aprovar nem reprovar.

**Regra:** D passa se nenhum critério falhar em nenhuma família. Se passar, a M2 fica resolvida no desenvolvimento e na
validação, e a reserva final avalia a v0.53 completa, uma vez. Se falhar, as falhas são declaradas e nada é ajustado.
Todas as famílias são medidas até o fim.
