# D2 da v0.55 — rascunho 3 (B6), só cenários sintéticos com sementes novas: plano (commitado antes de rodar)

**Data:** 16/10/2026.

**Protótipo:** lebre-research `experiments/LEBRE-V0.55-PROTO-01`, commit **`e375ec4`**, num worktree fixo. O script
recusa rodar com outro commit ou com a pasta alterada.

**Origem:** a D1 (`analises/D1_V055_RESULTADO.md`) reprovou B4 só na precisão. O diagnóstico descritivo mostrou que B4
barra unidades internas quando a memória é fraca. O responsável escolheu medir o rascunho 3 só em sintéticos e guardar
as séries reais nunca usadas para a validação e a avaliação final.

**Variantes:**
- **A:** v0.54 canônica;
- **B4:** a da D1, usada como **comparador** para a checagem de validade do banco;
- **B6:** a candidata: unidades externas testadas contra a previsão do núcleo, unidades internas contra s.

**Status:** desenvolvimento. O banco E20 não é usado, porque já respondeu à pergunta na D1.

## 1. Células

**Sementes:**
- séries: `default_rng([2026101700 + c, k])`;
- bootstrap: `[2026101720, c]`;
- ensaio: `[2026101690 + c, 0]`.

Todas na faixa reservada 2026101500–2026102999 e conferidas como não usadas em 16/10/2026.

As células 0 a 8 são as da D1, com a **mesma geração** e as sementes novas acima: N1, N2, N3, N4, N5, P1, P2, P3, P4.
Os tamanhos são os mesmos (60 ou 80 séries; T = 4.000 ou 8.000).

**Novas células de memória fraca** (o mecanismo da falha da D1), com T = 8.000 e n = 40:

| c | Célula | Geração | Ciclo declarado | Referência |
|---|---|---|---|---|
| 9 | W1: ciclo declarado errado + entrada | y = AR(0,5) + 1,0·sen(2πt/24) + 0,3·x0(t − 3); x0 a x3 AR(0,5) | 30 | sazonal |
| 10 | W2: ciclo declarado errado, sem entrada | y = AR(0,5) + 1,0·sen(2πt/24); x0 a x3 AR(0,5) | 30 | sazonal |
| 11 | W3: ciclo não declarado + entrada | igual a W1 | nenhum | persistência |
| 12 | W4: tipo solar | c = AR(0,95) (nebulosidade); y = max(0, sen(2πt/24))·(1 + 0,3·c) + 0,05·ruído; x0 = c + 0,3·ruído; x1 a x3 AR(0,5) | 30 | sazonal |

## 2. Medidas

As mesmas da D1, por série e variante:
- entradas externas no fim e alguma vez aceitas;
- passo da primeira aceitação de x0;
- x0 no fim;
- MSE nos últimos 2/3;
- custo por passo.

**Precisão por célula:** a razão MSE(variante) ÷ MSE(A) por série. O resumo é a média geométrica das razões, com IC 95%
por bootstrap das séries (4.000 réplicas, percentil).

## 3. Critérios (para B6)

| Código | Critério | Passa se |
|---|---|---|
| D2-a | espúrias em séries integradas | N1 e N2: limite superior de Clopper–Pearson ≤ 0,10 em cada célula, e a contagem de B6 < a de A na soma |
| D2-b | nulos estacionários | N3, N4 e N5: 0 de 80 com alguma entrada externa aceita (limite superior ≤ 0,05) |
| D2-d | retenção do genuíno | fração com x0 no fim ≥ a de A − 0,05 em P1, P2, P3, W1, W3 e W4 |
| D2-e | atraso de detecção | P1: mediana ≤ 1,5 × a de A |
| D2-f | precisão | em **toda** célula, limite superior do IC da razão B6 ÷ A ≤ 1,02 |
| D2-g | custo | mediana por série da razão de custo B6 ÷ A ≤ 1,25 |

**Checagem de validade do banco (pré-declarada).** As células W reproduzem o mecanismo da D1 se o limite superior do IC
de B4 ÷ A passar de 1,02 em pelo menos uma delas. Se nenhuma reproduzir, D2-f é reportado como "banco sem o mecanismo".
Nesse caso, B6 não pode ser dado como aprovado em precisão, e essa parte da decisão fica para os dados reais.

**Decisão:**
- **passa:** todos os critérios D2-a a D2-g, com o banco válido. B6 segue para a validação em séries reais nunca usadas,
  com plano próprio, a combinar com o responsável;
- **falha:** o resultado negativo é registrado;
- **banco inválido, mas o resto passa:** B6 segue para a validação real com a precisão em aberto, e isso é declarado.

Nada é ajustado depois de ver os resultados.

## 4. Execução

- `python -m analises.d2_v055 ensaio`, só para conferir que o script roda; o resultado não é usado;
- `python -m analises.d2_v055 sint`;
- `python -m analises.d2_v055 resumo`.

Variável de ambiente: `LEBRE055_PROTO` (pasta do worktree no commit `e375ec4`).
