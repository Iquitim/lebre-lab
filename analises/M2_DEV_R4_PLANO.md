# Medição da M2, rascunho 4, no banco de desenvolvimento: plano (escrito e commitado antes de rodar)

**Data:** 08/10/2026. **O quê:** protótipo da v0.53 no commit `432ef71` do lebre-research (o script registra o commit e
o hash de `model053.py`), especificação `ALGORITHM_SPEC_DRAFT_M2_r4.md`: AdaHedge (como no rascunho 2) sobre a perda
recortada da v0.52, min(e² / B², 1), B = CLIP_K × max(menor desvio recente dos dois previsores, piso). Auditoria como no
rascunho 2. **Onde:** as mesmas 23 famílias (22 + CURTAS, com o adendo 1 de `M2_DEV_R2_PLANO.md`), só desenvolvimento.

## 1. Configuração

Uma só, **K**, sem parâmetros livres.

## 2. Critérios e incerteza

Idênticos aos de `M2_DEV_R2_PLANO.md`: 1 (negativas, M2 ÷ ref, limite superior <= 1,01), 2 (19 positivas, C05
incluída, M2 ÷ v0.52 <= 1,02), 4, 5 (acréscimo de custo <= 75 FP por passo; a especificação estima ~74, no limite), 6 e
7 (CURTAS, M2 ÷ melhor <= 1,05). Mesmo bootstrap (B = 2000; blocos 168, 20, 12; em CURTAS 24, 20, 12), semente 20261012.

## 3. Regra (fixada antes)

K é escolhida se atender a todos os critérios. Se não atender: falhas declaradas, nada ajustado, volta à especificação.
Nenhuma família vira limitação declarada. A medição pode ser interrompida quando a regra já estiver decidida (falha
confirmada); nesse caso as famílias não medidas são listadas.

## 4. Conferências

v0.52 contra o registro do Lab; em C05 e B06, a configuração H do rascunho 2 tem de reproduzir `m2dev_r2/`.
