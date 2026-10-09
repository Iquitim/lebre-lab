# Diagnóstico E21 (M5): de onde vem o custo da v0.53, plano antes de rodar

**Data:** 09/10/2026. Só descrição, dados já gastos. Código: cópia fixa `bca5dac` (M1 r5 + M2 Q2). Uma série por família
(a primeira) das 64 do desenvolvimento ampliado. Custo médio por passo (regra de contagem da v0.52) separado em: v0.52 por
categoria (`memory`, `structure`, `experiments`, `screening`, `control`); M2 (`fp_porta`); M1: atualizações da RLS, resto do
especialista (triagem, seleção, previsão e recorte) e AdaHedge. Serve para escolher reduções de custo que **preservem as
previsões** (a M5 aceita só mudanças cuja saída fique igual à validada, sem gastar dados novos).
