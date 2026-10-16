# D1 da v0.55 — resultado

**Plano:** `analises/D1_V055_PLANO.md` (commit `d0865d8`, antes de rodar). **Protótipo:** lebre-research `324d667`, num
worktree fixo. **Execução:** única, 16/10/2026, depois do ensaio declarado no plano. Saídas: `d1_v055/sint.json`,
`d1_v055/e20.json` e `d1_v055/resumo.json`.

## Decisão pela regra pré-registrada

| Critério | B4 (principal) | B5 (secundária) |
|---|---|---|
| D1-a espúrias em séries integradas | **passa** | falha |
| D1-b nulos estacionários | passa | passa |
| D1-d retenção do genuíno | passa | passa |
| D1-e atraso de detecção | passa (mediana 930 contra 895) | passa (1.130 contra 895) |
| D1-f precisão no E20 (nenhum limite superior > 1,02) | **falha:** YB01 1,127; B03 1,045; YB06 1,033 | falha: YB01 1,109; A07 1,085; YB06 1,028; A01 1,026; A11 1,026 |
| D1-g custo (mediana ≤ 1,25) | passa (1,000) | passa (1,042) |
| Previsões não finitas | 0 | 0 |

**Nenhuma das duas passa.** Pela regra, o resultado negativo é registrado. O desenho volta ao diagnóstico, e não haverá
nova medição neste banco com estas sementes.

## Células sintéticas

| Célula | Medida | A (v0.54) | B4 | B5 |
|---|---|---|---|---|
| N1 passeio + entradas que passeiam (60) | séries com entrada externa no fim | **26** | **0** | 0 |
| N2 passeio + entradas AR(0,95) (60) | idem | 2 | 0 | 3 |
| N3 AR nulo (80) | séries com alguma externa aceita | 0 | 0 | 0 |
| N4 sazonal nulo (80) | idem | 0 | 0 | 0 |
| N5 quebra de variância (80) | idem | 0 | 0 | 0 |
| P1 verdadeira (60) | x0 no fim | 60 | 60 | 60 |
| P2 verdadeira + isca (60) | x0 no fim / isca alguma vez | 60 / 1 | 60 / 1 | 60 / 0 |
| P3 I(1), entrada nas diferenças (60) | x0 no fim | 57 | **49** | 45 |
| P4 cointegração (60) | x0 no fim / outras externas alguma vez | 57 / 14 | 59 / 0 | 49 / 8 |

O MSE das células nulas é praticamente igual nas três variantes (por exemplo, N1 1,0054 nas três). Em N1, a v0.54
termina com entrada espúria em 43% das séries, sem ganho de precisão nenhum.

**Descritivo pré-declarado: níveis do E20** (séries com entrada externa na estrutura final, 4 por família):

| Família | C03 | VC03 | WC03 | XC03 | YC03 |
|---|---|---|---|---|---|
| A | 4 | 3 | 3 | 4 | 2 |
| B4 | 0 | 0 | 0 | 0 | 0 |
| B5 | 0 | 0 | 0 | 0 | 0 |

## Banco E20 (B4 ÷ A)

- Mediana por série: 1,000.
- Séries com razão > 1,01: 4,8%; com razão < 0,99: 3,0% (728 séries).
- Média geométrica > 1 em 18 famílias e < 1 em 14.
- As três famílias que reprovam: YB01 (solar, validação 4), B03 (qualidade do ar) e YB06 (eólica, validação 4).

## Diagnóstico (descritivo, depois de ver os resultados; não muda a decisão)

**Pior série, YB01 "Conj. Lapa" (razão 1,22).** A e B4 terminam sem entrada externa nenhuma.
- **Na v0.54**, a unidade "passado do próprio alvo" (own_past, com bandas de atraso) é aceita no passo 4.040. O peso da
  estrutura fica em 0,98.
- **Em B4**, ela nunca é aceita. O peso da estrutura cai para 0,80, e a M1 assume (peso 0,70).
- **Causa:** a pergunta de B4 ("melhora a previsão do núcleo, que já contém a memória?") exclui por construção o passado
  do próprio alvo, que a memória já usa. Nessa família, porém, a memória está mal servida: o ciclo foi declarado como 30
  em vez de 24, erro de construção já registrado em `ERRATA_SEASON_VALIDACOES_4_5.md`. A estrutura precisava dessa
  unidade.

**Leitura.** B4 resolve o que pretendia, as entradas **externas** espúrias em séries integradas. Mas ela também barra
unidades **internas** (o passado do alvo e, possivelmente, o estado residual) que melhoram a previsão viva quando a
memória é fraca. Em B03 (C6H6) as estruturas externas diferem, e a perda não foi diagnosticada série a série.

**Outro custo:** em P3 (I(1) com entrada genuína nas diferenças), B4 retém x0 em 49 de 60 séries, contra 57 de 60 na
v0.54.

**Hipótese para um próximo desenho** (não testada; exige dados ou sementes novos):
- testar as unidades **externas** contra a previsão do núcleo (B4);
- testar as unidades **internas** (passado do alvo, estado residual, divisões delas) contra s, como na v0.54.

A motivação da M3 é a interpretação de entradas externas ("a entrada explica o alvo além do seu próprio passado").
Ela não se aplica ao próprio passado.
