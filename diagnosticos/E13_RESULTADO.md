# Diagnóstico E13: as três falhas da validação 4 (resultado)

**Data:** 09/10/2026. Plano `E13_PLANO.md` (commit `0304d03`). Só descrição, sobre dados já gastos. Dados brutos:
`e13_m2.json`, `e13_m1.json`, `e13_f6/`, `E13_F6_RESULTADO.md`.

## A. M2 contra a referência (excesso relativo de MSE; + = pior que a referência)

| Série | excesso | do Prod (P − D) | de D (D − R) | dos 1% passos mais extremos | peso de L em M |
|---|---|---|---|---|---|
| Y-C01 baht | +2,36% | +1,34% | +1,02% | +1,48% (todo no 2º meio, 1997) | 1,00 |
| Y-C01 dólar de Singapura | +0,47% | −0,14% | +0,62% | +0,04% | 0,47 |
| Y-C01 iene, coroa | ~0 | ~0 | ~0 | ~0 | ~0 |
| Y-B07 Portland | +0,23% | +0,23% | 0 | −0,85% | 0,50 |
| C01 petróleo (desenv., passou) | +1,27% | +1,26% | 0 | +1,27% | 0,00 |
| X-C01 (val. 3, passou) | −5,7% a +0,4% | ~0 | | | |

Leitura: o excesso grande (baht, petróleo) vem de **poucos passos extremos** e em boa parte do **Prod**. O Prod mede as
perdas **recortadas** em [0, 1] (garantia só nessa escala); num choque, a perda recortada de qualquer previsor vale 1 e o
Prod não distingue quem errou muito de quem errou absurdamente, mas o MSE distingue. Petróleo tem a mesma assinatura em
C01 e passou só porque as outras séries da família compensaram. Portland: excesso pequeno (0,23%); a falha vem sobretudo
da largura do intervalo com uma série só.

## B. M1 em Y-B01

Em 5 das 6 usinas o especialista nunca ganha peso (s ~ 0) e o efeito é nulo. Em **Horizonte** ele domina o tempo todo
(s médio 0,94) e piora o MSE em 19,5%, de forma crescente ao longo de 2025, concentrada no **nascer e pôr do sol** (16-17 h:
+22%; 6-7 h: +4%); nas horas de sol pleno ele até melhora. Mesma assinatura da parte A: o Prod da M1 também decide por
perda recortada e por isso prefere o especialista que ganha em muitos passos pequenos, mesmo perdendo muito nos poucos
passos de transição, que dominam o MSE.

Achado de dados (não causa da falha): o ONS tem valores impossíveis em Y-B01: Horizonte 543 MW (capacidade 79,8) em
09/09/2025 10 h; São Pedro até 803 MW (capacidade 54) em 31/12/2025. Ficam como estão (dados congelados); declarados.

## C. A F6 é geral? (v0.52 ÷ comparador linear online completo, média geométrica por família)

**B03 é um caso extremo:** 2,076 (até 5,5 numa série). As demais famílias com comparador melhor por mais de 5%: VB07
1,170, XB07 1,141, VC05 1,138 (uma série 2,5), YB03 1,225, YB06 1,095, B07 1,067, A05 1,077. Em 40 das 59 famílias a v0.52 é
melhor ou igual (<= 1,05); nas de carga, níveis e solar, muito melhor (0,24 a 0,83). A F6 existe fora de B03, mas é de
5-20% (marés, eólica de Y, Pequim), não de 2x.

## Causa comum (hipótese para os próximos rascunhos, não conclusão)

As garantias do Prod (M1 e M2) valem em **perda recortada**; o critério é **MSE**. Quando os erros têm cauda pesada ou
transições raras e grandes, ganhar em perda recortada não implica ganhar em MSE. Direção a examinar na literatura:
combinação com garantia na própria escala do erro quadrático (algoritmos sem limite de escala conhecido, "scale-free" ou
de faixa adaptativa), em vez de recortar.
