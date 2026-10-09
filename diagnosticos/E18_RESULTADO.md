# Auditoria E18: previsões NaN não contadas (resultado)

Plano `E18_PLANO.md`.

| Config | Família | Série | passos NaN / avaliação | primeiro |
|---|---|---|---|---|

Séries afetadas / auditadas: prod: 0 / 728; prod_q: 0 / 728; prod_r2: 0 / 90

**Leitura:** nenhuma previsão NaN em nenhuma série auditada (P, Q e P + M1 r2). O defeito do subagregador M existia, mas não
foi disparado em nenhuma medição registrada; nenhuma errata é necessária. A correção (lebre-research `fc71880`) fica, e as
métricas continuam descartando passos não finitos: a auditoria passa a ser repetida em toda medição futura.
