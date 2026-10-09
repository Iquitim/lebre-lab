# Diagnóstico E14: a v0.52 está abaixo da fronteira precisão × custo onde o comparador linear a vence? Plano antes de rodar

**Data:** 09/10/2026. **Só descrição**, sobre dados já gastos. Motivação: E13, parte C (`E13_RESULTADO.md`): o comparador
linear online completo vence a v0.52 por mais de 5% em 8 famílias (B03, B07, VB07, VC05, XB07, YB03, YB06, A05), mas custa
20 a 60 vezes mais. A pergunta é se a v0.52 perde para algo **do mesmo custo** (defeito) ou só para algo muito mais caro
(preço do orçamento).

**Medição (`e14_fronteira.py`):** em cada série das 8 famílias, a v0.52 e as 8 variantes de RLS do E10 (AR2+0, AR2+B3,
AR2+B-todas, completo; a cada passo e a cada 8; mesmas classes e fórmula de custo de `f6_e10.py` e `m1_val4_alvo.py`),
erro = MSE ÷ MSE do comparador completo. Por família: média geométrica do erro de cada previsor e custo médio por passo.

**Classificação declarada antes:** com c = custo médio da v0.52 na família e e* = menor erro entre as variantes com
custo <= c: **abaixo da fronteira** se erro da v0.52 > 1,05 × e* (a mesma tolerância de 5% do critério de F6); **na
fronteira** caso contrário. Também reportado: a razão para a melhor variante com custo <= 2,5 c (o teto da M1).

**Leitura combinada (antes de ver):** abaixo da fronteira em várias famílias além de B03 → F6 é estrutural e a M1 deve
ser geral; só em B03 → F6 em B03 é específica, e o restante é preço do orçamento, a declarar como limite de escopo da
v0.53 e problema a tratar na v0.54.
