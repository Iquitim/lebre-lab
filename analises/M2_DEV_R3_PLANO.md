# Medição da M2, rascunho 3, no banco de desenvolvimento: plano (escrito e commitado antes de rodar)

**Data:** 08/10/2026. **O quê:** protótipo da v0.53 no commit `bda07f4` do lebre-research (o script registra o commit e
o hash de `model053.py`), especificação `ALGORITHM_SPEC_DRAFT_M2_r3.md`: saída = média ponderada de R e L com pesos do
Fixed Share, α_t = 1/t (Adamskiy et al., 2016, Corolário 6), sobre a perda logarítmica de previsões gaussianas
N(previsão, σ²), σ² = média exponencial (0,99) dos erros quadráticos do próprio previsor. Auditoria como no rascunho 2.
**Onde:** as mesmas 23 famílias do rascunho 2 (22 + CURTAS, com o adendo 1 de `M2_DEV_R2_PLANO.md`), só desenvolvimento.

## 1. Configuração

Uma só, **S**, sem parâmetros livres. Auditoria: α_porta = 0,01, ε 0,002, recriada, observa na quarentena por entradas.

## 2. Critérios e incerteza

Idênticos aos de `M2_DEV_R2_PLANO.md` (critérios 1, 2 com C05 incluída, 4, 5 com limite 75 FP por passo, 6 e 7 para
CURTAS com limite superior <= 1,05 contra o melhor entre v0.52 e referência), mesmo bootstrap (B = 2000; blocos 168, 20,
12 e, em CURTAS, 24, 20, 12), semente 20261011. O resultado também informa se o limite antigo de custo (25) passaria.

## 3. Regra (fixada antes)

S é escolhida se atender a todos os critérios. Se não atender: as falhas são declaradas, nada é ajustado, e volta-se à
especificação. **C05 e CURTAS não viram limitação declarada:** a condição do responsável pelo projeto é resolvê-las.

## 4. Conferências

- A v0.52 tem de reproduzir o MSE do registro do Lab.
- Em C05 e B06, a configuração H (AdaHedge) do rascunho 2 é rodada de novo e tem de reproduzir o MSE de `m2dev_r2/`.

## 5. Também reportado (não decide)

Peso médio de L; em C05, primeiro passo com peso de L > 0,9; variação média do peso por passo; eventos de auditoria;
cobertura do intervalo da saída; CURTAS por origem.
