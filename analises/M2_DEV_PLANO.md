# Medição da M2 (v0.53) no banco de desenvolvimento: plano (escrito e commitado antes de rodar)

**Data:** 07/10/2026. **O quê:** o protótipo da v0.53 com a porta da referência trivial (M2), em
`lebre-research/experiments/LEBRE-V0.53-PROTO-01` (commit `da200a1`; o script registra o commit e o hash de
`model053.py` usados). Especificação: `ALGORITHM_SPEC_DRAFT_M2.md`, rascunho 0. **Onde:** só cenários do LEBRE Lab
(dados de desenvolvimento); nada da reserva da v0.53.

## 1. Configurações (ablação da seção 6 da especificação, completa)

| | ε_porta = 0 | ε_porta = 0,002 | ε_porta = 0,005 |
|---|---|---|---|
| hipóteses recriadas ao fim do episódio | R0 | R2 | R5 |
| hipóteses persistentes | P0 | P2 | P5 |

Escala do recorte fixa no erro do vigente (como a v0.52). Nenhuma outra escolha é variada.

## 2. Famílias e referência

- **Negativas** (a v0.52 perde para a referência): C01, C03, C04.
- **Positivas** (a v0.52 vence a referência; as 19 do D04/D05): A01-A12, B01, B02, B03, B06, B07, C02, C05.
- **Referência** da porta e das comparações: zero quando o cenário a declara (C01, C04), sazonal ingênuo quando há ciclo
  declarado, persistência nos demais (mesma regra de `lab/m2.py`).
- A v0.52 é rodada pela cópia do protótipo com a porta desligada (idêntica bit a bit à `lebre==0.1.0`, ver testes do
  protótipo), e o MSE dela é conferido contra o registro do Lab.

## 3. Critérios (os da especificação, seção 7)

1. Em C01, C03 e C04: limite superior do intervalo de 95% da razão M2 ÷ referência <= 1,01.
2. Nas 19 famílias positivas: limite superior do intervalo de 95% da razão M2 ÷ v0.52 <= 1,02.
3. Alternância: média de trocas de modo por 2.000 passos <= 1, em cada família.
4. Mudanças falsas: em A02, C01 e C04, número de séries com alguma entrada externa aceita não maior que o da v0.52.
5. Custo: acréscimo médio <= 25 FP por passo, em cada família.

**Incerteza:** bootstrap de blocos móveis pareado dentro de cada série, como em `INCERTEZA_PLANO.md`; blocos de 168
(horárias), 20 (sintéticas e dias úteis) e 12 (mensais); B = 2000; semente 20261008. Mesmos limites declarados
(séries tratadas como independentes).

## 4. Regra de escolha (fixada antes)

- Entre as configurações que atendem aos 5 critérios, escolher a de menor média geométrica de M2 ÷ referência nas três
  famílias negativas; empate (diferença < 0,001) decide pela menor ε_porta e, depois, por "recriadas".
- Se nenhuma atender aos 5 critérios: **nenhuma é escolhida**; registrar quais critérios falharam e voltar à
  especificação antes de qualquer outro ajuste (não testar novos valores fora da grade da seção 1).

## 5. Também reportado (não decide)

Tempo até a primeira promoção nas famílias positivas; recall em A01-A12 contra a v0.52 (a porta compartilha a sequência
e-LOND e pode alterar decisões estruturais); cobertura do intervalo da saída.
