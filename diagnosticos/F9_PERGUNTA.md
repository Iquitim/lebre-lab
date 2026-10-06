# Diagnóstico F9 (níveis de preço): a melhora que levou às aceitações existiu?

Escrito e commitado antes de rodar (06/10/2026). Exploratório; limite absoluto de 20 minutos.

**Dados:** as 4 séries do cenário C03 (níveis de dólar/real, euro/dólar, iene/dólar e petróleo WTI, 2010-2025). Nada
da reserva da v0.53.

**Método:** em cada série rodam duas LEBREs congeladas (`lebre==0.1.0`): a normal (com as 5 entradas de C03) e uma sem
entradas externas (uma entrada constante igual a zero; só memória e intercepto). Para cada entrada externa aceita no
passo t, razão de MSE (normal ÷ sem entradas) nos 250 dias úteis antes de t e nos 250 depois.

**Regra de decisão (por aceitação):**
- razão antes < 1 e depois >= 1: **existiu e sumiu** (relação passageira);
- razão antes >= 1: **nunca existiu** (o teste se enganou);
- razão antes < 1 e depois < 1: **existiu e ficou**.

**Consequência:** maioria "existiu e sumiu" leva a priorizar remoções e persistência (M4); maioria "nunca existiu" leva a
priorizar testar sobre as variações (M3); maioria "existiu e ficou" indica que a aceitação ajudou localmente e que a
perda contra o passeio aleatório vem de outra parte (memória e modelo base, como em F8).
