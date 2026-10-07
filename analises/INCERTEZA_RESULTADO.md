# Incerteza dos resultados centrais: resultado

Plano: `INCERTEZA_PLANO.md` (commitado antes do cálculo). Bootstrap de blocos móveis pareado dentro de cada série, B = 2000, semente 20261007; intervalo de 95% por percentis da média geométrica da família.

## Reprodutibilidade

| Família | Maior diferença relativa de MSE contra as execuções originais |
|---|---|
| B01 | 0.0e+00 |
| B02 | 0.0e+00 |
| B03 | 0.0e+00 |
| B06 | 0.0e+00 |
| B07 | 0.0e+00 |
| C01 | 0.0e+00 |
| C02 | 0.0e+00 |
| C03 | 0.0e+00 |
| C04 | 0.0e+00 |
| C05 | 0.0e+00 |

## Comparações

| Família | Comparação | Séries | Razão (média geom.) | IC 95% | Séries < 1 | Leitura |
|---|---|---|---|---|---|---|
| B01 | lebre/linear_online | 6 | 0.721 | 0.705–0.738 | 6 de 6 | consistente: melhor |
| B01 | lebre/sazonal_ingenuo | 6 | 0.231 | 0.223–0.239 | 6 de 6 | consistente: melhor |
| B01 | porta/lebre | 6 | 1.000 | 1.000–1.000 | 0 de 6 | confirmado (<= 1,02) |
| B02 | lebre/linear_online | 4 | 0.473 | 0.460–0.487 | 4 de 4 | consistente: melhor |
| B02 | lebre/sazonal_ingenuo | 4 | 0.036 | 0.035–0.037 | 4 de 4 | consistente: melhor |
| B02 | porta/lebre | 4 | 1.000 | 1.000–1.000 | 0 de 4 | confirmado (<= 1,02) |
| B03 | lebre/linear_online | 4 | 2.076 | 1.904–2.300 | 0 de 4 | consistente: pior |
| B03 | lebre/sazonal_ingenuo | 4 | 0.113 | 0.103–0.124 | 4 de 4 | consistente: melhor |
| B03 | porta/lebre | 4 | 1.000 | 1.000–1.000 | 0 de 4 | confirmado (<= 1,02) |
| B06 | lebre/linear_online | 6 | 1.017 | 1.009–1.026 | 1 de 6 | consistente: pior |
| B06 | lebre/sazonal_ingenuo | 6 | 0.117 | 0.112–0.121 | 6 de 6 | consistente: melhor |
| B06 | porta/lebre | 6 | 1.000 | 1.000–1.000 | 0 de 6 | confirmado (<= 1,02) |
| B07 | lebre/linear_online | 6 | 1.067 | 1.054–1.079 | 1 de 6 | consistente: pior |
| B07 | lebre/ingenuo | 6 | 0.941 | 0.929–0.953 | 3 de 6 | consistente: melhor |
| B07 | porta/lebre | 6 | 0.978 | 0.971–0.984 | 4 de 6 | confirmado (<= 1,02) |
| C01 | lebre/linear_online | 4 | 1.020 | 0.978–1.066 | 1 de 4 | inconclusivo |
| C01 | lebre/zero | 4 | 1.069 | 1.035–1.104 | 0 de 4 | consistente: pior |
| C01 | porta/zero | 4 | 1.015 | 1.004–1.031 | 0 de 4 | consistente: pior |
| C02 | lebre/linear_online | 4 | 0.999 | 0.952–1.028 | 3 de 4 | inconclusivo |
| C02 | lebre/ingenuo | 4 | 0.602 | 0.566–0.623 | 4 de 4 | consistente: melhor |
| C02 | porta/lebre | 4 | 1.007 | 1.000–1.015 | 0 de 4 | confirmado (<= 1,02) |
| C03 | lebre/linear_online | 4 | 0.559 | 0.508–0.613 | 4 de 4 | consistente: melhor |
| C03 | lebre/ingenuo | 4 | 1.068 | 1.041–1.087 | 0 de 4 | consistente: pior |
| C03 | porta/ingenuo | 4 | 1.038 | 1.009–1.057 | 0 de 4 | consistente: pior |
| C03 | lebre/sem_entradas | 4 | 0.992 | 0.979–1.000 | 4 de 4 | inconclusivo |
| C04 | lebre/linear_online | 3 | 1.005 | 0.969–1.046 | 2 de 3 | inconclusivo |
| C04 | lebre/zero | 3 | 1.052 | 1.013–1.098 | 1 de 3 | consistente: pior |
| C04 | porta/zero | 3 | 1.003 | 0.991–1.016 | 1 de 3 | inconclusivo |
| C05 | lebre/linear_online | 2 | 0.897 | 0.781–0.994 | 2 de 2 | consistente: melhor |
| C05 | lebre/ingenuo | 2 | 0.895 | 0.837–0.970 | 2 de 2 | consistente: melhor |
| C05 | porta/lebre | 2 | 1.000 | 1.000–1.000 | 0 de 2 | confirmado (<= 1,02) |

Leitura conforme a seção 3 do plano. Para porta ÷ referência (C01, C03, C04), a margem de 1% do D04 só é confirmada se o limite superior for <= 1,01. Limites do método: seção 4 do plano (séries tratadas como independentes; intervalos tendem a ser estreitos demais quando as séries compartilham o tempo).

## Leitura contra o que o Lab tinha dito (escrita depois do cálculo)

**Confirmado com intervalo:** LEBRE melhor que o linear online em B01 (0,72), B02 (0,47), C03 (0,56) e C05 (0,90);
pior em B03 (2,08, F6); melhor que a referência ingênua em todas as famílias reais e em C02 e C05; pior que a previsão
trivial em C01 (1,07), C03 (1,07) e C04 (1,05), que é F8. A porta (M2) não piora mais de 2% onde a LEBRE vence: limite
superior de no máximo 1,015 em todas as famílias medidas.

**Correções:**
1. **B06 (eólica) não é empate com o linear online.** Razão 1,017 (IC 1,009–1,026), pior em 5 de 6 usinas: a LEBRE é
   ligeiramente **pior**, 1,7%. O critério de B06 (até 1,05) continua atendido, mas o texto "empate" no MAPA estava
   impreciso.
2. **A margem de 1% da porta em C04 não está confirmada.** O D04 deu 1,003 no ponto, mas o intervalo (0,991–1,016)
   passa de 1,01. Em C01 e C03 a porta é **consistentemente pior** que a referência (limites inferiores 1,004 e 1,009),
   como o D04 já indicava.
3. **B07 (marés):** no conjunto das 6 estações a LEBRE é **consistentemente melhor** que a persistência (0,941; IC
   0,929–0,953), embora perca em 3 das 6 estações. F7 continua valendo por estação, mas não para a família.

**Inconclusivo (o Lab tinha dito empate, o que é compatível):** LEBRE contra o linear online em C01, C02 e C04; LEBRE
contra a LEBRE sem entradas em C03 (0,992; IC 0,979–1,000), coerente com o diagnóstico F9 ("menos de 1%").

**Não coberto aqui:** os cenários sintéticos (A01-A12) e o D05a/b; ali a variação vem de muitas sementes e a contagem por
série já foi reportada.
