# Medição da M2, rascunho 2, no banco de desenvolvimento: plano (escrito e commitado antes de rodar)

**Data:** 08/10/2026. **O quê:** protótipo da v0.53 no commit `82e7b16` do lebre-research (o script registra o commit e
o hash de `model053.py`), especificação `ALGORITHM_SPEC_DRAFT_M2_r2.md`: a saída é a média ponderada da referência (R)
e da LEBRE (L), com pesos de AdaHedge ou FlipFlop (de Rooij et al., 2014) sobre a perda quadrática; a porta do rascunho
1 continua só como auditoria. **Onde:** as 22 famílias das medições anteriores e uma família nova de séries curtas; só
dados de desenvolvimento, nada da reserva da v0.53.

**Condição do responsável pelo projeto:** nenhuma versão é promovida sem resolver C05. Aqui, "resolver" é o critério 2
em C05 (limite superior do IC 95% de M2 ÷ v0.52 <= 1,02), fixado antes de rodar.

## 1. Configurações

| Config | Saída | Parâmetros | Auditoria |
|---|---|---|---|
| H | AdaHedge | nenhum | porta do rascunho 1, α_porta = 0,01, ε 0,002, recriada, observa na quarentena por entradas |
| F | FlipFlop | φ = 2,37, α = 1,243 (Corolário 16 do artigo) | idem |

Prioridade uniforme (½, ½). Nenhum parâmetro é ajustado. O α_porta da auditoria não afeta a saída; fica em 0,01 (a
proposta do rascunho 1).

## 2. Famílias

- **As 22 de antes:** negativas C01, C03, C04; positivas A01-A12, B01, B02, B03, B06, B07, C02, C05; nulas A02, C01,
  C04. Mesma regra de referência (zero se declarada, sazonal se há ciclo, senão persistência).
- **Família nova "CURTAS"** (para que a solução não seja feita sob medida para C05): os primeiros 360 passos de cada
  série de B01, B02, B03, B06, B07, C01, C02, C03 e C04 (o Lab não tem B04 nem B05), mais C05 inteira (360 meses). Cada
  série curta é rodada do zero (v0.52, referência e M2), avaliada a partir do passo int(0,2 × 360) = 72.

## 3. Critérios

1. Em C01, C03 e C04: limite superior do IC 95% de M2 ÷ referência <= 1,01.
2. Nas 19 famílias positivas, **C05 incluída**: limite superior do IC 95% de M2 ÷ v0.52 <= 1,02.
3. (Alternância) não se aplica a pesos contínuos; reportada a variação média |Δw_L| por passo, sem decidir.
4. Em A02, C01 e C04: número de séries com entrada externa aceita não maior que o da v0.52.
5. Custo: acréscimo médio <= **75** FP por passo, em cada família. **Revisão declarada antes de rodar:** o limite de 25
   dos rascunhos 0 e 1 foi fixado para uma porta sem agregação; a recontagem da agregação com a regra de FP da v0.52 dá
   48 FP por passo (constante `FP_AGREGACAO_PASSO`, comentada no protótipo), que somados aos ~18 da auditoria dão ~66.
   O limite 25 falharia por construção, e isso é dito aqui, não descoberto depois. O resultado reporta também se o
   limite antigo passaria. A aceitação do novo limite é decisão do responsável pelo projeto.
6. Caminho estrutural idêntico ao da v0.52 em todas as séries (eventos, exceto os da auditoria, e custo da parte v0.52).
7. **CURTAS:** limite superior do IC 95% de M2 ÷ melhor(v0.52, referência) <= 1,05, em que "melhor" é, em cada série, o
   de menor MSE na janela de avaliação (escolha a posteriori, ou seja, um comparador otimista).

**Incerteza:** bootstrap de blocos móveis pareado, B = 2000, semente 20261010; blocos 168 (horárias), 20 (sintéticas e
dias úteis), 12 (mensais), como antes. Na família CURTAS, a janela de 288 passos não comporta blocos de 168; usa-se 24
nas horárias, 20 nas de dias úteis e 12 em C05. Agregação por família: média geométrica das razões e IC pela média dos
log-razões das réplicas entre séries (como nas medições anteriores).

## 4. Regra de escolha (fixada antes)

Entre as configurações que atendem aos critérios 1, 2, 4, 5, 6 e 7, a de menor média geométrica de M2 ÷ melhor(v0.52,
referência) sobre as 23 famílias; empate (< 0,001) decide pelo AdaHedge (mais simples). Se nenhuma atender: nenhuma é
escolhida, as falhas são declaradas e, como diz a especificação, volta-se à literatura (Fixed Share, Squint), **sem
ajustar parâmetros**. C05 não vira limitação declarada nesta rodada: a condição do responsável pelo projeto é resolvê-la.

## 5. Conferências

- A v0.52 (protótipo com a porta desligada) tem de reproduzir o MSE do registro do Lab nas 22 famílias.
- Nas famílias C05 e B06, a configuração A1 do rascunho 1 é rodada de novo; o MSE por série tem de ser igual ao de
  `m2dev_r1/`.

## 6. Também reportado (não decide)

Peso médio de L na janela de avaliação; em C05, primeiro passo com peso de L > 0,9; trocas de regime do FlipFlop;
eventos de auditoria; cobertura do intervalo da saída.
