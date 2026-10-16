# D3 da v0.55 — rascunho 4 (B7), só cenários sintéticos com sementes novas: plano (commitado antes de rodar)

**Data:** 16/10/2026.

**Protótipo:** lebre-research `experiments/LEBRE-V0.55-PROTO-01`, commit **`8ba6dc8`**, num worktree fixo.

**Origem:** a D2 (`analises/D2_V055_RESULTADO.md`) reprovou B6 só na retenção em P3. O diagnóstico mostrou que, numa
série integrada, a informação de uma entrada verdadeira não chega à previsão, nem na v0.54 nem em B6. O rascunho 4 (B7)
acrescenta a estrutura de inovação como terceiro especialista aninhado.

**Variantes:**
- **A:** v0.54;
- **B6:** a da D2, comparador;
- **B7:** a candidata.

## 1. Células

**Sementes:**
- séries: `default_rng([2026101800 + c, k])`, c = 0 a 14;
- bootstrap: `[2026101820, c, v]`;
- ensaio: `[2026101770 + c, 0]`.

Todas na faixa reservada e conferidas como não usadas.

**Errata da D2 (declarada aqui, antes de rodar a D3).** No ensaio da D2, a base 2026101690 + c, com c = 10 a 12 (as
células W2, W3 e W4), deu as sementes `[2026101700 a 2026101702, 0]`. Essas são as das séries k = 0 de N1, N2 e N3 da
execução principal, ou seja, houve reuso de semente entre o ensaio e a execução. Não há efeito no resultado da D2: o
ensaio não foi usado, e as células geram séries diferentes a partir do mesmo gerador. Na D3, a base do ensaio é
2026101770, sem sobreposição.

**Células 0 a 12:** as da D2, com a mesma geração e as sementes novas acima: N1 a N5, P1 a P4, W1 a W4.

**Células novas** (T = 8.000, n = 60, referência de persistência):

| c | Célula | Geração |
|---|---|---|
| 13 | P5: I(1) com efeito forte | Δy = 1,0·x0(t − 1) + 0,5·ruído; x0 a x3 AR(0,5) |
| 14 | P6: I(1) com entrada verdadeira e espúrias | Δy = 0,5·x0(t − 2) + 0,5·ruído; x0 AR(0,5); x1 a x3 passeios aleatórios independentes |

## 2. Medidas

As mesmas da D2: precisão por célula pela média geométrica das razões de MSE (variante ÷ A) nos últimos 2/3, com IC 95%
por bootstrap das séries.

## 3. Critérios (para B7)

Todos os da D2, com as mesmas definições:
- **D3-a** (= D2-a): espúrias em N1 e N2;
- **D3-b** (= D2-b): nulos N3 a N5;
- **D3-d** (= D2-d): retenção ≥ a de A − 0,05, agora em P1, P2, P3, **P5, P6**, W1, W3 e W4;
- **D3-e** (= D2-e): atraso de detecção em P1;
- **D3-f** (= D2-f): precisão, todo limite superior ≤ 1,02;
- **D3-g** (= D2-g): custo, mediana ≤ 1,25.

Mais dois:

| Código | Critério | Passa se |
|---|---|---|
| D3-h | a informação chega à previsão em série integrada | em P3 e P5, limite superior do IC 95% da razão B7 ÷ A < 1,00 |
| D3-i | ficar com a verdadeira e rejeitar as espúrias ao mesmo tempo | P6: séries com alguma entrada externa diferente de x0 no fim: limite superior de Clopper–Pearson ≤ 0,10 |

No script, os critérios D3-a, D3-b, D3-d, D3-e, D3-f e D3-g aparecem com os rótulos "D2-a" a "D2-g", herdados do script
da D2.

**Decisão:**
- **passa:** todos os critérios. B7 segue para a validação em séries reais nunca usadas, com plano próprio, a combinar
  com o responsável;
- **falha:** o resultado negativo é registrado.

Nada é ajustado depois de ver os resultados.

## 4. Execução

`python -m analises.d3_v055 ensaio | sint | resumo`, com `LEBRE055_PROTO` no worktree do commit `8ba6dc8`.
