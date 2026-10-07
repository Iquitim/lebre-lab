# Incerteza dos resultados centrais do LEBRE Lab: plano (escrito e commitado antes de calcular)

**Data:** 07/10/2026. **Por quê:** quase todas as conclusões do Lab se apoiam em 2 a 6 séries por família, sem intervalo
de confiança. Este plano fixa, antes de qualquer cálculo, quais comparações serão medidas, como e como serão lidas.

## 1. Comparações (lista fechada)

| Família | Comparação | Afirmação do Lab que ela confere |
|---|---|---|
| B01, B02, B03, B06, B07 | LEBRE ÷ linear online | Ganho ou perda contra o linear online (fase 2) |
| B01, B02, B03, B06 | LEBRE ÷ sazonal ingênuo; B07: LEBRE ÷ ingênuo | Ganho sobre a referência ingênua |
| C01, C04 | LEBRE ÷ zero | F8: perda contra prever zero |
| C03 | LEBRE ÷ ingênuo (passeio aleatório) | F9/F8: perda contra o passeio aleatório |
| C03 | LEBRE ÷ LEBRE sem entradas externas | Diagnóstico F9: efeito das entradas espúrias |
| C02, C05 | LEBRE ÷ ingênuo | Ganho em volatilidade e inflação mensal |
| C01, C03, C04 | porta (M2) ÷ referência | Protótipo de M2: quanto da perda a porta recupera |
| B01, B02, B03, B06, B07, C02, C05 | porta (M2) ÷ LEBRE | Protótipo de M2: a porta não piora onde a LEBRE vence |

A porta é exatamente a do D04/D05 (`lab/ensembles.py`, `Porta`, alfa = 0,01), com a mesma regra de referência
(`lab/m2.py`). Nenhum modelo, dado ou parâmetro é ajustado aqui.

## 2. Estatística e incerteza

- **Por série:** razão de MSE depois do aquecimento (20% iniciais), só nos passos com alvo e as duas previsões finitas.
- **Por família:** média geométrica das razões das séries (média dos logaritmos), como no Lab.
- **Incerteza:** bootstrap de blocos móveis dentro de cada série, reamostrando juntos os erros dos dois modelos
  comparados (preserva a dependência no tempo e o pareamento). Blocos de 168 passos (dados horários), 20 (dias úteis) e
  12 (mensais). B = 2000 réplicas, semente 20261007. Em cada réplica, a estatística da família é a média dos
  logaritmos das razões das séries. Intervalo de 95% por percentis.
- **Também reportado:** quantas séries da família têm razão abaixo de 1.

## 3. Regra de leitura (fixada antes)

- "A melhor que B" só é dito **consistente** se o intervalo de 95% da razão A ÷ B ficar todo abaixo de 1; "pior", se
  ficar todo acima de 1; caso contrário, **inconclusivo**.
- Para "não piora mais de 2%" (porta ÷ LEBRE): **confirmado** se o limite superior do intervalo for <= 1,02.
- Para "recupera a perda" (porta ÷ referência nos testes negativos): reportar o intervalo; a margem de 1% do D04 é
  confirmada só se o limite superior for <= 1,01.

## 4. Limites declarados do método

- O bootstrap trata as séries de uma família como independentes. Usinas próximas e sites de prédios compartilham o
  tempo; a dependência entre séries tende a deixar os intervalos **estreitos demais**.
- O bootstrap mede a incerteza amostral no tempo, não a incerteza de escolha dos cenários e das séries (que são poucas).
- Com 2 a 6 séries, a média geométrica da família depende muito de cada série; por isso a contagem por série é
  reportada junto.

## 5. Conferência de reprodutibilidade (embutida)

As previsões são recalculadas. Como a LEBRE e os comparadores são determinísticos e os dados são os do manifesto
(`dados/MANIFESTO_SHA256.tsv`), o MSE recalculado de cada modelo em cada série tem de ser igual ao registrado nas
execuções originais (B01-B07, C01-C05, D04, D05). Qualquer diferença acima de 1e-9 (relativa) é reportada como falha
de reprodutibilidade, e a comparação afetada não é lida.
