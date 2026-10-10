# Diagnóstico E23: linha de base da v0.53 para as prioridades da v0.54. Resultado

**Data:** 10/10/2026. Plano: `E23_PLANO.md` (commit `c8275a9`, com o script, antes de rodar).
Biblioteca `lebre==0.2.0` do PyPI (v0.53) e o núcleo sozinho (`core_only=True`). Só descritivo. Dados brutos:
`e23_base_v054.json`.

## 1. Custo (prioridade 1)

| Cenário | Núcleo (FP/passo) | v0.53 | parte da M1 | parte da M2 | peso final da M1 | v0.53 ÷ núcleo (MSE) |
|---|---|---|---|---|---|---|
| A01, d = 10 (10 séries) | 760 | 1.706 | 808 | 137 | 0 em 10/10 | 1,000 |
| A01, d = 20 (10 séries) | 1.253 | 2.205 | 814 | 137 | 0 em 10/10 | 1,000 |
| A01, d = 50 (10 séries) | 3.161 | 4.131 | 833 | 137 | 0 em 10/10 | 1,000 |
| A12, d = 50, T = 200 mil | 3.164 | 4.138 | 837 | 137 | 0 | 1,000 |
| A05 (20 séries, d = 3) | 385 | 924 | 401 | 137 | 0 em 20/20 | — |
| C03 (4 séries) | 596 | 1.453 | 725 | 132 | 0 em 4/4 | — |

- O custo do **núcleo** continua crescendo com o número de entradas (F1): 760 → 3.161 de d = 10 a 50, com recall 1,00 e
  nenhuma entrada falsa.
- A **M1** custa ~400 a ~840 FP por passo (cresce com m = mín(d, 5)) e terminou com **peso zero em todas as 95 séries
  medidas aqui** (A01, A02, A05, A12 e C03), sem mudar o erro.
- **Avaliação final da v0.53** (arquivo publicado, nenhuma execução nova): a M1 terminou com peso zero em **70 de 104**
  séries (todas as de solar, eólica, carga e câmbio; 25 de 30 prédios; 1 de 30 bacias), com acréscimo mediano de 800 FP
  e custo mediano de 2,25 vezes o do núcleo nessas séries. Nelas, a razão v0.53 ÷ núcleo foi 1,000, exceto no câmbio
  (0,966 em retornos e 0,952 em níveis), onde o ganho vem da M2. O ganho da M1 ficou concentrado em 34 séries (29
  bacias, 5 prédios). Ressalva: "peso final zero" descreve o fim da série; o peso pode ter sido positivo antes.

## 2. Remoções (prioridade 2, M4) — A05

- A entrada antiga x0 foi removida em **0 de 20** séries e está na estrutura final em **20 de 20**.
- Erro 7,7% acima do linear online (média geométrica), igual na v0.53 e no núcleo (estrutura idêntica em 20/20; a M1
  ficou com peso zero).

## 3. Interpretação em séries não estacionárias (prioridade 2, M3) — C03

| Série | entrada externa aceita | estrutura final | v0.53 ÷ ingênuo | núcleo ÷ ingênuo |
|---|---|---|---|---|
| dólar/real | sim | x1 | 1,000 | 1,045 |
| euro/dólar | sim | x0 | 1,000 | 1,030 |
| iene/dólar | sim | x2 | 1,000 | 1,050 |
| petróleo WTI | sim | x0 | 1,009 | 1,153 |

A M2 resolveu a precisão (de 3% a 15% pior que o passeio aleatório para 0% a 0,9%), mas a interpretação continua como
antes: **4 de 4** séries com entrada externa espúria aceita e mantida até o fim.

## 4. Controle — A02

Nenhuma entrada falsa em 40 séries nulas; estrutura idêntica à do núcleo em 40/40.

## 5. Ciclo (prioridade 3, M6) — séries de D02

| Grupo | séries | v0.53 sem ciclo ÷ com o ciclo certo | núcleo, idem |
|---|---|---|---|
| Carga (ciclo certo 24 + 168) | 4 | 2,872 | 2,883 |
| Solar (ciclo certo 24) | 6 | 1,435 | 1,435 |
| Todas | 10 | 1,894 | 1,897 |

Sem declarar o ciclo, a v0.53 erra 2,9 vezes mais na carga e 1,4 vez mais na solar; a M2 (referência persistência,
sem ciclo) praticamente não compensa.

## Leitura para a nota de desenho da v0.54 (sem decidir nada)

- A maior parte do custo novo da v0.53 é a M1 trabalhando com peso zero: um custo proporcional ao uso (M5) aplicado
  também às camadas atacaria ~800 FP na mediana de 2/3 das séries da avaliação final, sem tocar no ganho, se a regra
  souber reativar a M1 quando ela voltar a ajudar.
- O crescimento com d (F1) continua sendo do núcleo.
- M4, M3 e M6 têm alvos claros e medidos acima.
