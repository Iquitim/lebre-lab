# Auditoria E18: previsões NaN não contadas (subagregador M), plano antes de rodar

**Data:** 09/10/2026. Achado ao testar a Q2 (lebre-research, teste `test_q2_escala_volta_depois_de_um_pico`): o
subagregador M (`SwitchMonotono`, usado pelas candidatas P, Q e Q2 da M2) produz NaN quando toda a massa da posterior está
de um lado e esse lado perde por uma margem enorme (0/0 por underflow); daí em diante a saída fica NaN. As métricas do Lab
(`forecast_metrics`, `par_bootstrap`) **descartam em silêncio** os passos com previsão não finita, então uma série afetada
seria avaliada só até o NaN.

**Auditoria (`e18_nan.py`), com o código atual do protótipo (sem correção):** em todas as séries das 64 famílias (as 59 e
as cinco curtas), P (`saida="prod"`), Q (`"prod_q"`) e, nas famílias Y, P + M1 r2 (a configuração da validação 4): número de
passos do período de avaliação com alvo finito e previsão não finita, e o primeiro passo. Resultado decide quais medições
registradas precisam de errata.
