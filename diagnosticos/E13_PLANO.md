# Diagnóstico E13: as três falhas da validação 4, plano antes de rodar

**Data:** 09/10/2026. **Só descrição**, sobre dados já gastos (desenvolvimento e validações 1 a 4); não muda nenhuma
decisão registrada. Serve para orientar os próximos rascunhos da M1 e da M2, que serão confirmados numa validação 5 nova.
Protótipo: lebre-research `experiments/LEBRE-V0.53-PROTO-01` no commit atual (código da M1 r2 e da P sem mudanças).

## A. M2 (candidata P) contra a referência: de onde vem o excesso (`e13_m2.py`)

Séries: Y-C01 (4) e Y-B07 Portland (falharam); controles que passaram: C01 (desenvolvimento) e X-C01 (validação 3).
M2 sem M1. Para cada série, no período de avaliação (t >= 20% de T, alvo observado), com R = referência, D e M = os dois
subagregadores, P = saída:
1. excesso relativo (Σ(P−y)² − Σ(R−y)²) / Σ(R−y)², decomposto em parcela do Prod (P contra D) e parcela de D (D contra R);
2. concentração: fração do excesso vinda dos 1% de passos com maior (R−y)², e do primeiro contra o segundo meio;
3. médias de s (fração do Prod em M) e do peso de L em D e em M.

Hipóteses a examinar (não testes): H1, o excesso vem de poucos passos extremos (por exemplo, a crise asiática de 1997 no
baht), onde a perda quadrática de D, sem limite, paga caro pelo peso residual em L; H2, vem do Prod (mistura com M).

## B. M1 em Y-B01 Horizonte (`e13_m1.py`)

M1 + M2 contra M2 sozinha, nas 6 séries de Y-B01 (Horizonte é a que falhou). Excesso por mês e por hora do dia; fração
do excesso nos passos em que o especialista tem s > 0,5; número de passos em que a previsão do especialista bate no recorte
L ± B; checagem dos dados (fração de zeros, trechos constantes, mudanças de nível).

## C. A F6 é geral? (`e13_f6.py`)

Em todas as séries do desenvolvimento e das validações 1 a 4: MSE da v0.52 ÷ MSE do comparador linear online completo
(o mesmo do critério de F6), com d e custo do comparador. Pergunta: em quantas famílias o comparador vence a v0.52 por
mais de 5% (média geométrica da família)? B03 é um caso isolado?
