# D4 da v0.55 — rascunho 5 (B8), só cenários sintéticos com sementes novas: plano (commitado antes de rodar)

**Data:** 16/10/2026.

**Protótipo:** lebre-research `experiments/LEBRE-V0.55-PROTO-01`, commit **`2f250bf`**, num worktree fixo.

**Origem:** a D3 (`analises/D3_V055_RESULTADO.md`) reprovou B7 na retenção em P6 e no critério de informação em P5.
Um diagnóstico descritivo nas séries já gastas da P6 mostrou o mecanismo: com wS = 0, as vagas de experimento eram
ocupadas por testes de unidades internas contra s, que não podem mudar a previsão. Os passeios concorrentes não eram a
causa (a hipótese anterior estava errada). O rascunho 5 (B8) não abre teste novo de unidade interna enquanto wS < 0,05.

**Variantes:**
- **A:** v0.54;
- **B7:** a da D3, comparador;
- **B8:** a candidata.

## 1. Células e sementes

As 15 células da D3 (N1 a N5, P1 a P6, W1 a W4), com a mesma geração (`analises/d4_v055.py` é o `d3_v055.py` com as
trocas abaixo) e sementes novas:
- séries: `default_rng([2026101900 + c, k])`;
- bootstrap: `[2026101920, c, v]`;
- ensaio: `[2026101870 + c, 0]`, sem sobreposição com as da execução.

Todas na faixa reservada e conferidas como não usadas em 16/10/2026.

## 2. Critérios (para B8)

Os da D3, com as mesmas definições: D4-a, D4-b, D4-d, D4-e, D4-f e D4-g. No script, aparecem com os rótulos herdados
"D2-a" a "D2-g". A retenção (D4-d) vale em P1, P2, P3, P5, P6, W1, W3 e W4. Mais estes dois:

| Código | Critério | Passa se |
|---|---|---|
| D4-h | a informação chega à previsão em série integrada | em **P3 e P6**, limite superior do IC 95% da razão B8 ÷ A < 1,00 |
| D4-i | P6: espúrias no fim | limite superior de Clopper–Pearson ≤ 0,10 |

**Mudança de critério feita depois de ver a D3, declarada aqui com o motivo.** Na D3, o critério de informação (D3-h)
usava P3 e P5. Em P5, a v0.54 já estava a 6% do piso teórico (MSE 0,2645 contra 0,25), e o critério ficava quase
inatingível por construção. No D4-h, P5 é trocada por P6, onde a v0.54 está 29% acima do piso. P5 continua coberta pelos
critérios de precisão (D4-f) e de retenção (D4-d).

**Decisão:**
- **passa:** todos os critérios. B8 segue para a validação em séries reais nunca usadas, com plano próprio, a combinar
  com o responsável;
- **falha:** o resultado negativo é registrado.

Nada é ajustado depois de ver os resultados.

## 3. Execução

`python -m analises.d4_v055 ensaio | sint | resumo`, com `LEBRE055_PROTO` no worktree do commit `2f250bf`.
