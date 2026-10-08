# Diagnóstico E9 de F6 (B03): resultado

| Série | d | v0.52 | L0 | L0Y | Q8 | TOP3 | COMPLETO |
|---|---|---|---|---|---|---|---|
| CO(GT) | 8 | 1.716 | 3.231 | 1.765 | 2.937 | 3.611 | 1.000 |
| NOx(GT) | 8 | 1.496 | 2.573 | 1.505 | 2.353 | 3.663 | 1.000 |
| NO2(GT) | 8 | 1.308 | 3.057 | 1.371 | 2.751 | 4.813 | 1.000 |
| C6H6(GT) | 8 | 5.533 | 2.441 | 2.295 | 2.040 | 4.672 | 1.000 |

Valores: MSE ÷ MSE do COMPLETO (o comparador linear online do Lab). TOP3 escolhido pela correlação no trecho de aquecimento (20% iniciais), só para o diagnóstico.

## Leitura

F6 **não** é um problema de relação exata no mesmo instante: só com as entradas no instante t, a própria RLS fica pior que
a v0.52 em CO, NOx e NO2 (2,6 a 3,2 vezes o comparador, contra 1,3 a 1,7 da v0.52). A vantagem do comparador linear vem da
estrutura conjunta de defasagens (alvo defasado e 8 defasagens de todas as entradas numa regressão com 75 variáveis): as
defasagens do alvo explicam a maior parte em CO, NOx e NO2; no benzeno (o caso extremo, 5,5 vezes), nenhuma variante
parcial chega perto do comparador completo. As 3 entradas no instante t (o especialista da M1 enxuta) são o pior desenho
possível aqui (3,6 a 4,8 vezes). O diagnóstico de F6 da nota de desenho estava errado e é corrigido aqui.
