# Candidata P da M2 na validação 3: plano, escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** a candidata P (`M2_CANDIDATA_P.md`, lebre-research; protótipo `saida="prod"`, código
do commit `5c81d07`, sem mudanças no protótipo desde então; o script registra o commit atual, `6e43d9a`, e o hash de
`model053.py`). **Onde:** a validação 3 congelada (`VALIDACAO3_CONGELADA.md`, commit `0b0a83a`), 41 séries em 9
famílias mais X-CURTAS, usada **uma única vez**.

**Régua:** por decidibilidade (`M2_CANDIDATA_D.md`): classificação v0.52 ÷ referência (semente 20261029); critério 1 nas
"referência melhor" (<= 1,01), 2 nas "v0.52 melhor" (<= 1,02), 4 em X-C01 e X-C04, 5 com **<= 150 FP por passo** (decisão
do responsável pelo projeto), 6 em todas, 7 em X-CURTAS (<= 1,05). Medição com semente 20261028.

**Regra:** P passa se nenhum critério falhar em nenhuma família. Se passar, a M2 fica resolvida no desenvolvimento e na
validação, e a reserva final avalia a v0.53 completa, uma vez. Se falhar, as falhas são declaradas e nada é ajustado.
Todas as famílias são medidas até o fim. Contagem declarada: P é a 12ª configuração da M2.
