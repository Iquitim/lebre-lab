# Banco fixo da v0.55 — rodada C1 (confirmação): resultado

**Plano:** `analises/BANCO_V055_PLANO.md`, §5, com a rodada C1 registrada no commit `de1022c`, antes de rodar.
**Candidata:** B10, congelada no commit `b0522a0` do lebre-research (o mesmo da D5, sem mudança). **Sementes:**
nunca usadas (base 2026102100). **Execução:** única, 17/10/2026. Saídas: `banco_v055_C1/sint.json` e
`banco_v055_C1/resumo.json`.

## Decisão: B10 CONFIRMADA em sintéticos

Todos os critérios passam:

| Critério | B10 |
|---|---|
| C-a espúrias | passa: N1 0/60 (A: 22); N2 0/60 (A: 3); passeios na Q7 0/40 (A: 22) |
| C-b nulos | passa: 0 nas 240 séries de N3, N4 e N5 |
| C-d retenção | passa, nenhuma célula abaixo de A − 0,05: P3 60 (A 56); P6 60 (A 48); Q5 76/80 (A 46) |
| C-e atraso | passa |
| C-f precisão | passa: pior limite superior 1,010 (P4) |
| C-g custo | passa: mediana 1,043 |
| C-h a informação chega à previsão | passa: P3 0,961 (até 0,972); P6 0,957 (até 0,969); conjunto das integradas **0,913 (0,907–0,918)** |

**Células novas (Q):** Q1 0,869; Q2 0,932; Q3 0,830; Q4 0,850; Q5 0,977; Q6 0,965; Q7 0,683; Q8 0,994.

**O que vem a seguir** (plano, §3): a validação em séries reais nunca usadas, com pré-registro próprio, no
lebre-research.
