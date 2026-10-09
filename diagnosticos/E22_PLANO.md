# Verificação E22 (M5): as mudanças de implementação preservam as previsões validadas? Plano antes de rodar

**Data:** 09/10/2026. Mudança (lebre-research `4a2620e`): o especialista da M1 simetriza cada par da matriz da RLS uma vez
e padroniza só a linha nova; a contagem de FP foi auditada (RLS 6k² + 5k; previsão 2k + 18m + 4; repadronização do buffer
na troca de entradas). **Critério:** o MSE de cada série da v0.53 (M1 r5 + M2 Q2), recalculado com o código novo, tem de
ser **exatamente igual** (igualdade de ponto flutuante) ao registrado com `bca5dac` no E20 (64 famílias) e na validação 5
(`analises/m1val5`). Reporta também o custo novo. Se alguma série diferir, a mudança não é aceita como redução sem
revalidação. Só verificação; não gasta dados novos (os da validação 5 já foram usados uma vez para a decisão e aqui só se
confere igualdade de saída).
