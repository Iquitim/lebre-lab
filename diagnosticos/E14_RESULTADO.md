# Diagnóstico E14: a v0.52 na fronteira precisão × custo (resultado)

Plano `E14_PLANO.md`. Erro = MSE ÷ comparador linear online completo (média geométrica da família); custo em FP por passo (média). e* = menor erro entre as variantes com custo <= o da v0.52; e*(2,5) = idem com custo <= 2,5 vezes.

| Família | séries | d | v0.52 (erro @ custo) | e* (variante) | v0.52 ÷ e* | e*(2,5) (variante) | v0.52 ÷ e*(2,5) | classificação |
|---|---|---|---|---|---|---|---|---|
| B03 | 4 | 8 | 2.076 @ 731 | 1.574 (AR2+B3/8, 318) | 1.319 | 1.302 (AR2+B-todas/8, 1574) | 1.594 | abaixo |
| B07 | 6 | 3 | 1.067 @ 431 | 1.004 (AR2+0/1, 282) | 1.062 | 1.004 (AR2+0/1, 282) | 1.062 | abaixo |
| VB07 | 6 | 3 | 1.170 @ 435 | 1.005 (AR2+0/1, 282) | 1.164 | 1.005 (AR2+0/1, 282) | 1.164 | abaixo |
| VC05 | 4 | 3 | 1.138 @ 262 | 1.381 (AR2+0/8, 72) | 0.824 | 1.000 (AR2+0/1, 282) | 1.138 | na fronteira |
| XB07 | 6 | 3 | 1.141 @ 417 | 1.010 (AR2+0/1, 282) | 1.130 | 1.010 (AR2+0/1, 282) | 1.130 | abaixo |
| YB03 | 4 | 10 | 1.225 @ 830 | 1.397 (AR2+B3/8, 318) | 0.877 | 1.397 (AR2+B3/8, 318) | 0.877 | na fronteira |
| YB06 | 6 | 5 | 1.095 @ 640 | 1.048 (AR2+0/1, 482) | 1.044 | 1.048 (AR2+0/1, 482) | 1.044 | na fronteira |
| A05 | 20 | 3 | 1.077 @ 385 | 1.777 (AR2+B-todas/8, 318) | 0.606 | 1.389 (COMPLETO/8, 750) | 0.775 | na fronteira |

## Leitura

**A F6 é estrutural, não só de B03.** A v0.52 está abaixo da fronteira em 4 das 8 famílias: B03 e as **três famílias de
maré independentes** (B07, VB07, XB07; desenvolvimento e validações 1 e 3), com repetição consistente (6-16%). Nas marés,
uma regressão **mais barata que a v0.52** (AR2+0 a cada passo: alvo defasado de 1 e 2 passos e as entradas no instante t,
estimados juntos, ~280 FP contra ~430) empata com o comparador completo. Em B03, o que basta é AR2 + bandas de 3 entradas a
cada 8 passos (318 FP). Em VC05, YB03, YB06 e A05 a v0.52 está na fronteira: perder para o completo ali é preço do orçamento.

Consequência para a M1: o especialista do rascunho 2 (AR2 + bandas de 5 entradas, a cada 8 passos) não cobre o caso das
marés, onde o ganho vem de estimar alvo defasado e entradas atuais **juntos e a cada passo**. A falha comum à v0.52 é não
estimar conjuntamente a dinâmica do alvo e o efeito das entradas.
