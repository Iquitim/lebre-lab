# Medição da M2, rascunho 1, no banco de desenvolvimento: plano (escrito e commitado antes de rodar)

**Data:** 08/10/2026. **O quê:** protótipo da v0.53 no commit `9bfdd0d` do lebre-research (o script registra o commit e
o hash de `model053.py`), especificação `ALGORITHM_SPEC_DRAFT_M2_r1.md`. **Onde:** as mesmas 22 famílias do Lab da
medição do rascunho 0 (`M2_DEV_PLANO.md`), só dados de desenvolvimento.

## 1. Configurações

| Config | α_porta | ε_porta | Hipóteses | Observa na quarentena por entradas |
|---|---|---|---|---|
| A1 | 0,01 | 0,002 | recriadas | sim |
| A5 | 0,05 | 0,002 | recriadas | sim |

## 2. Critérios

Os 5 de `M2_DEV_PLANO.md` (seção 3), com a mesma referência, incerteza (bootstrap de blocos pareado, B = 2000, semente
20261009, blocos 168/20/12) e famílias, mais:

6. **Caminho estrutural idêntico:** em todas as séries, eventos estruturais (exceto os da porta) e custo da parte v0.52
   exatamente iguais aos da v0.52 sem porta.

## 3. Regra de escolha (fixada antes)

Entre as configurações que atendem aos 6 critérios, a de menor média geométrica de M2 ÷ referência nas famílias
negativas; empate (< 0,001) decide pelo menor α_porta. Se nenhuma atender, nenhuma é escolhida; as falhas são
declaradas e, conforme a especificação, C05 vira limitação declarada se for a única falha (nada é ajustado para ele).

## 4. Conferência do rascunho 0

Em C05 e B06, a configuração R2 do rascunho 0 (motor compartilhado, sem observar na quarentena por entradas) é rodada de
novo com o protótipo atual; o MSE por série tem de ser igual ao registrado em `m2dev/` (rascunho 0).
