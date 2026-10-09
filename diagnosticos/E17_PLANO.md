# Diagnóstico E17: por que a M1 rascunho 3 piora algumas séries e não alcança a meta em VB07, plano antes de rodar

**Data:** 09/10/2026. **Só descrição**, sobre dados já gastos; não muda a decisão do E16. Séries: B01 Arinos 2 500 kV
(+42%), C05, WC05 ipca_habitacao, YC05 (inflação mensal, +1-3%), VB07 (1,084 contra meta 1,056) e B07 (atende, controle).
Medidas (`e17_m1.py`), no período de avaliação: MSE ÷ v0.52 da combinação L', do especialista recortado e do
especialista sem recorte; peso médio s; fração dos passos em que o recorte atua; excesso de L' sobre a v0.52 em cada
quinto do período.

Hipóteses (não testes): H1 (VB07): o recorte em ±2σ impede o especialista de chegar ao nível da regressão sozinha; H2
(inflação mensal, T = 300): com poucos passos, a fase de entrada e a escala do Prod (normalizada pelo maior erro) custam
mais que o ganho; H3 (Arinos): a usina começa a gerar no meio da série e o especialista, aprendido no trecho sem geração,
erra na transição.
