# Quando usar a LEBRE (mapa em construção)

Atualizado ao fim de cada fase, a partir do registro de execuções. Tudo aqui é **exploratório** (PLANO.md, regra 5).

## Depois da fase 1 (dados sintéticos com resposta conhecida, 2026-10-04)

Fonte: execuções de A01 a A12 em `runs/REGISTRO.csv`. Para A05, A06, A07 e A12 valem as execuções refeitas
(`runs/ANOTACOES.md`). Todas as séries têm entradas AR(1) e relações lineares conhecidas, salvo indicação.

### Onde ela se saiu bem

| Situação | O que se viu | Cenário |
|---|---|---|
| Muitas entradas irrelevantes (até 50) | Achou as 2 verdadeiras em 30 de 30 séries, sem falsas; erro 30 a 40% menor que o linear online | A01 |
| Nada a descobrir | 0 mudanças falsas em 40 séries | A02 |
| Atrasos de até 31 passos | Atraso 24 achado em 10 de 10, erro 59% menor que o linear online | A04 |
| Efeito que muda devagar, até de sinal | Entrada achada em 20 de 20; erro 4% menor que o linear online | A06 |
| Efeito que liga e desliga | Achada em 20 de 20, um único evento por série, erro 11% menor que o linear online | A07 |
| Dados faltando em blocos | Recall de 100%, 0 falsas, nenhuma previsão inválida | A08 |
| Outliers e sensor travado | Recall de 97,5%, 0 falsas | A09 |
| Relações não lineares monótonas (limiar, saturação) | Entrada achada em 10 de 10, erro parecido com o linear online | A10 |
| Ruído de cauda pesada ou que depende de outra entrada | 0 falsas, recall de 100%; a entrada que só muda a variância nunca foi aceita | A11 |
| Cobertura do intervalo de 90% | Entre 0,90 e 0,91 em todos os cenários | todos |

### Onde ela tem limites

| Situação | O que se viu | Cenário |
|---|---|---|
| Atrasos acima de 31 passos | Nunca descobertos (0 de 30), como previsto pelo desenho | A04 |
| Relação simétrica, como x² | Invisível (0 de 10): ela é linear | A10 |
| Entradas muito correlacionadas | Com 0,8, aceita a substituta junto com a verdadeira em 4 de 10; com 0,95, no lugar dela em 4 de 10 | A03 |
| Troca de regime | Aceita a nova entrada (atraso mediano de ~1.900 passos), mas nunca remove a antiga; erro 8% maior que o linear online | A05 |
| Muitas entradas: custo | ~760 operações por passo com 10 entradas, ~1.250 com 20, ~3.160 com 50 (contra ~400 com até 5) | A01, A12 |

### Leitura prática (provisória)

- Boa escolha quando há várias entradas candidatas e **algumas** delas importam com atraso de até 31 passos, inclusive
  com dados sujos (faltantes, outliers, caudas pesadas).
- Use com cuidado quando as relações mudam de lugar com frequência (trocas de regime), quando o efeito pode vir com
  atraso maior que 31 passos ou quando as entradas são quase cópias umas das outras.
- Com muitas entradas, o custo deixa de ser "algumas centenas de operações por passo".

## Depois da fase 2 (dados reais, 2026-10-04)

Fonte: execuções de B01, B02, B03, B06 e B07 em `runs/REGISTRO.csv` (B04 e B05 adiados: dados/FONTES.md). A meteorologia
é reanálise (o tempo que ocorreu), então os ganhos com entradas de tempo são otimistas em relação ao uso real.

| Domínio | Resultado | Erro da LEBRE ÷ linear online | Erro ÷ referência ingênua | Cenário |
|---|---|---|---|---|
| Carga elétrica (4 subsistemas do ONS) | atende | 0,47 | 0,04 (sazonal) | B02 |
| Geração solar (6 usinas) | atende | 0,72 | 0,23 (sazonal) | B01 |
| Geração eólica (6 usinas) | atende | 1,02 (empate) | 0,12 (sazonal) | B06 |
| Qualidade do ar (4 poluentes) | **não atende** | **2,08** (5,5 no benzeno) | 0,11 (sazonal) | B03 |
| Maré meteorológica (6 estações) | **não atende** | **1,07** | 0,94 (persistência); pior que ela em 3 de 6 | B07 |

A cobertura do intervalo de 90% ficou entre 0,901 e 0,903 em todos os domínios.

### Leitura

- **Onde ela brilha:** séries com ciclos fortes (carga, solar). A memória sazonal dela faz muito do trabalho que o
  linear online não faz.
- **Onde perde:** quando a relação com uma entrada **no mesmo instante** é quase exata (benzeno e o sensor de NMHC, com
  correlação 0,98). O modelo base dela se ajusta devagar (NLMS) e fica atrás de uma regressão recursiva (RLS), que
  aprende o mapeamento com precisão. Também perde para a persistência em parte das estações de maré, onde o sinal é
  lento e as entradas ajudam pouco.
- **Cuidado ao ler "entradas aceitas":** o valor atual de todas as entradas já entra no modelo base sem decisão
  nenhuma. A lista de aceitas mostra só o que ela passou a usar **com atraso** (de 1 a 31 passos). Na eólica, por
  exemplo, a velocidade do vento quase nunca aparece como aceita, provavelmente porque o efeito dela é no mesmo
  instante e já está no modelo base.
