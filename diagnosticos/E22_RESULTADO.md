# Verificação E22 (M5): resultado

Plano `E22_PLANO.md`.

Séries conferidas: 813; com MSE diferente do registrado: 0.

Custo contado novo ÷ antigo: mediana 1.032 (mín 1.000, máx 1.042).

**Leitura:** as mudanças de implementação da M5 (lebre-research `4a2620e`) preservam bit a bit as previsões validadas
(813 de 813 séries com MSE idêntico). A contagem auditada eleva o custo **contado** em ~3% (mediana 1,032): os custos
reportados antes estavam um pouco subestimados; a partir daqui vale a contagem nova. Nenhuma medição precisa ser refeita
(as decisões dependem de MSE, que não mudou; o custo foi sempre só reportado, e o teto de F6 de 2,5 vezes continua
atendido: o maior custo nas famílias de F6 sobe de ~2,21 para ~2,28 vezes a v0.52).
