# Medição da M2, rascunho 5, no banco de desenvolvimento: plano (escrito e commitado antes de rodar)

**Data:** 08/10/2026. **O quê:** protótipo da v0.53 no commit `244f7b3` do lebre-research (o script registra o commit e
o hash de `model053.py`), especificação `ALGORITHM_SPEC_DRAFT_M2_r5.md`: Fixed Share com taxas variáveis (Cesa-Bianchi
et al., 2012, eq. 13; α_t = 2/(t+1); η_t pela regra do AdaHedge) sobre a perda recortada do rascunho 4. Auditoria como no
rascunho 2. **Onde:** as mesmas 23 famílias, só desenvolvimento.

## 1. Configuração

Uma só, **Q**, sem parâmetros livres.

## 2. Critérios, incerteza e regra

Idênticos aos de `M2_DEV_R4_PLANO.md` (critérios 1, 2 com C05, 4, 5 com 75 FP por passo, 6 e 7), semente 20261013.
Q é escolhida se atender a todos; senão, falhas declaradas, nada ajustado. Risco declarado antes de rodar (especificação,
seção 2): concentração mais fraca dos pesos onde a LEBRE é claramente melhor. A medição pode ser interrompida quando a
regra já estiver decidida, com as famílias não medidas listadas.

## 3. Conferências

v0.52 contra o registro do Lab; em C05 e B06, a configuração H do rascunho 2 tem de reproduzir `m2dev_r2/`.
