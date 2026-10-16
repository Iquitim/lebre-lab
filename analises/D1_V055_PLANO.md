# D1 da v0.55 — medição de desenvolvimento do núcleo ancorado: plano (commitado antes de rodar)

**Data:** 16/10/2026.

**Protótipo:** lebre-research `experiments/LEBRE-V0.55-PROTO-01`, commit **`324d667`**, num `git worktree` fixo. O script
recusa rodar com outro commit ou com a pasta alterada.

**Desenho:** `experiments/LEBRE-V0.55-DESIGN-NOTE-01/DESIGN_NOTE.md` (rascunho 0 mais o adendo 01). O teste de fumaça
que escolheu as variantes está em `experiments/LEBRE-V0.55-PROTO-01/FUMACA_RESULTADO.md`.

**Variantes**, todas com a mesma M1, M2, M4 e M5 da v0.54:
- **A:** v0.54 canônica;
- **B4:** a referência dos testes passa a ser a previsão combinada do núcleo; a previsão viva é a da v0.54. É a
  candidata **principal**;
- **B5:** B4 com a cópia lenta da estrutura (μ_ref = 0,01, assentamento de 500 passos) dentro da referência. É a
  candidata **secundária**.

**Status:** desenvolvimento. Nenhum resultado aqui é evidência vinculante. A promoção exige a validação em dados nunca
vistos e a avaliação final da v0.55.

## 1. Cenários sintéticos (verdade conhecida)

O alvo e as entradas são gerados pelo script. A semente de cada série é `default_rng([2026101600 + c, k])`, com c o
índice da célula na tabela abaixo (0 a 8) e k = 0, …, n − 1. Essas sementes foram conferidas como não usadas em
16/10/2026 e pertencem à faixa reservada 2026101500–2026102999.

| c | Célula | Geração | T | n | Referência da M2 |
|---|---|---|---|---|---|
| 0 | N1: passeio + entradas que passeiam | y e 5 entradas: passeios aleatórios independentes, incrementos N(0, 1) | 4.000 | 60 | persistência |
| 1 | N2: passeio + entradas persistentes | y passeio; 5 entradas AR(0,95) independentes | 4.000 | 60 | persistência |
| 2 | N3: AR estacionário nulo | y AR(1) ρ = 0,8; 4 entradas AR(0,5) independentes | 8.000 | 80 | persistência |
| 3 | N4: sazonal nulo | y = AR(1) ρ = 0,5 + 1,0·sen(2πt/24); 4 entradas AR(0,5); ciclo declarado 24 | 8.000 | 80 | sazonal |
| 4 | N5: quebra de variância nula | y AR(1) ρ = 0,8, ruído ×3 a partir de T/2; 4 entradas AR(0,5) | 8.000 | 80 | persistência |
| 5 | P1: entrada verdadeira | y = 0,3·x0(t − 3) + 0,3·ruído; x0 a x3 AR(0,5) | 8.000 | 60 | persistência |
| 6 | P2: verdadeira + isca | P1 com x1 = 0,7·x0 + 0,71·ruído AR(0,5) (correlação ~0,7) | 8.000 | 60 | persistência |
| 7 | P3: I(1) com entrada nas diferenças | Δy = 0,5·x0(t − 2) + 0,5·ruído; x0 a x3 AR(0,5) | 8.000 | 60 | persistência |
| 8 | P4: cointegração | x0 passeio; y = x0 + AR(0,5); x1 a x3 passeios independentes | 8.000 | 60 | persistência |

**Medidas por série e variante:**
- entradas externas (x\*) na estrutura **final**;
- entradas externas **alguma vez** aceitas;
- passo da primeira aceitação de x0 (células P);
- presença de x0 no fim;
- MSE nos últimos 2/3;
- custo por passo.

## 2. Banco E20 do Lab (precisão)

São as 64 famílias e 728 séries já usadas no desenvolvimento e na auditoria da v0.54 (teste T10), com a mesma função de
bootstrap pareado por blocos (`m2_dev.par_bootstrap`) e os mesmos blocos e janela inicial (20%) do E20.

- Semente do bootstrap: `[2026101610, índice da família, k, v]`, com v = 1 para B4 e v = 2 para B5.
- Razão por série: MSE da variante ÷ MSE de A.
- Resumo por família: média geométrica, e IC 95% pela média das réplicas em log, como no T10.

## 3. Critérios (para B4 e, separadamente, para B5)

IC de Clopper–Pearson 95% bilateral para as frações.

| Código | Critério | Passa se |
|---|---|---|
| D1-a | espúrias em séries integradas (N1, N2) | fração de séries com entrada externa na estrutura final: limite superior ≤ 0,10 **em cada célula**, e a contagem da variante < a de A na soma de N1 e N2 |
| D1-b | nulos estacionários (N3, N4, N5) | fração de séries com **alguma** entrada externa aceita: limite superior ≤ 0,05 em cada célula (equivale a 0 de 80) |
| D1-d | retenção do genuíno (P1, P2) | fração com x0 na estrutura final ≥ a de A − 0,05 em cada célula |
| D1-e | atraso de detecção (P1) | mediana do passo da primeira aceitação de x0 (séries em que as duas variantes aceitam) ≤ 1,5 × a de A |
| D1-f | precisão no E20 | em **nenhuma** família o limite superior do IC 95% da razão passa de 1,02 (o sinal de alerta do T10) |
| D1-g | custo no E20 | mediana por série da razão de custo (variante ÷ A) ≤ 1,25 |

**Só descritivos, sem critério:**
- P2: aceitação da isca;
- P3 e P4: retenção de x0. A v0.54 pode falhar aqui, e o resultado mostra se a mudança ajuda ou atrapalha;
- custo de pico;
- espúrias em C03 e nas demais famílias de níveis do E20 (estrutura final).

**Decisão para cada variante:**
- **passa:** todos os critérios D1-a, D1-b, D1-d, D1-e, D1-f e D1-g;
- se B4 passa, ela segue para o rascunho de especificação e a validação em dados nunca vistos;
- se B4 falha e B5 passa, segue B5;
- se as duas falham, o resultado negativo é registrado e o desenho volta ao diagnóstico, sem nova medição neste banco
  com as mesmas sementes.

Nada é ajustado depois de ver os resultados.

## 4. Execução

- `python -m analises.d1_v055 sint` (células sintéticas);
- `python -m analises.d1_v055 e20` (banco E20);
- `python -m analises.d1_v055 resumo` (critérios).

Ambiente: `.venv` do Lab (CPython 3.11, NumPy 2.2.5). Variáveis de ambiente:
- `LEBRE055_PROTO`, `LEBRE054_PROTO` e `LEBRE053_PROTO`: pastas do mesmo worktree no commit `324d667`.

**Ensaio, antes da execução principal e fora dela:** 1 série por célula com sementes `[2026101590 + c, 0]`, mais a
primeira família do E20. Serve só para conferir que o script roda. O resultado do ensaio não é usado. Se o ensaio revelar
um defeito de script, a correção é commitada e declarada antes da execução principal.
