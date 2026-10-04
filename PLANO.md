# LEBRE Lab: plano

Objetivo: testar a versão congelada da LEBRE (biblioteca `lebre==0.1.0`, algoritmo v0.52-r1) em situações novas, para
saber **onde ela funciona, onde falha e por quê**. Os resultados alimentam três coisas: um guia de quando usar a LEBRE,
exemplos prontos por domínio e uma lista priorizada de falhas para a próxima versão.

Este projeto é **exploratório**. Ele não substitui a avaliação pré-registrada da pesquisa e não gera afirmações
publicáveis sozinho (ver a regra 5).

## 1. Regras

1. **A versão congelada não muda.** Usamos `lebre==0.1.0` instalada do PyPI. Se aparecer um bug, ele é registrado em
   `FALHAS.md`, nunca corrigido aqui.
2. **Pergunta e critério antes de rodar.** Cada cenário declara, no próprio arquivo, a pergunta, o que esperamos e o
   critério de sucesso. O arquivo é commitado **antes** da execução, e o executor se recusa a rodar um cenário com
   alterações não commitadas. O registro guarda o commit usado.
3. **Todo teste rodado entra no registro** (`runs/REGISTRO.csv`), inclusive os que deram errado, foram abortados ou
   ficaram inconclusivos. Nada é apagado; uma execução corrigida é uma nova linha que cita a anterior.
4. **Sempre com comparadores simples** (seção 3). Sem comparação, "funcionou" não diz nada.
5. **Afirmação pública exige confirmação.** Se um resultado exploratório parecer forte o bastante para ser divulgado
   como resultado, ele é repetido com pré-registro e dados reservados, como na v0.52. Até lá, é descrito como
   exploratório.
6. **Dados só com licença conferida.** Antes de baixar um conjunto, registramos a fonte, a licença e se ela permite
   redistribuição (`dados/FONTES.md`). Dados brutos não entram no git.
7. **Mercado financeiro: nenhuma promessa de ganho.** Medimos qualidade de previsão, não lucro de estratégia. Um
   backtest de operação com custos é outro projeto.

## 2. As três frentes

### Frente A: estresse com resposta conhecida (dados sintéticos)

A verdade é conhecida, então dá para medir exatamente o que ela acerta e onde quebra. Sem problema de licença; é a
primeira frente a rodar.

| ID | Cenário | Pergunta |
|---|---|---|
| A01 | Muitas entradas: d = 10, 20, 50, só 2 relevantes | Ela acha as relevantes? Quanto custa por passo? |
| A02 | Só entradas irrelevantes (cenário nulo) | Quantas mudanças falsas ela aceita? |
| A03 | Substitutas correlacionadas (ρ = 0,5; 0,8; 0,95) | Com que frequência aceita a substituta no lugar da verdadeira? |
| A04 | Atrasos longos (24, 48, 96, 200 passos) | Até que atraso ela descobre o efeito? |
| A05 | Mudança de regime abrupta (a entrada relevante troca) | Em quanto tempo ela remove a antiga e aceita a nova? |
| A06 | Deriva gradual do coeficiente | Ela acompanha ou fica para trás? |
| A07 | Efeito intermitente (aparece e some) | Ela entra e sai na hora certa ou oscila? |
| A08 | Dados faltando em blocos (alvo e entradas) | A previsão e as decisões degradam com elegância? |
| A09 | Outliers e sensor travado | Um sensor travado leva a decisões erradas? |
| A10 | Relação não linear (limiar, saturação) | Quanto se perde por ela ser linear? |
| A11 | Ruído de cauda pesada e heterocedástico | O controle de mudanças falsas se mantém? |
| A12 | Escala: 10^6 passos, d = 50 | Custo por passo, memória e tempo real |

### Frente B: novos domínios com dados reais e abertos

Cada cenário só roda depois de a licença ser conferida.

| ID | Domínio | Alvo e entradas (candidatos) |
|---|---|---|
| B01 | Energia solar | Geração fotovoltaica; irradiância, temperatura, nebulosidade |
| B02 | Carga elétrica | Carga (ONS); temperatura e umidade (INMET) |
| B03 | Qualidade do ar | Poluentes (UCI Air Quality); meteorologia, sensores vizinhos |
| B04 | Dengue | Casos semanais (InfoDengue); chuva e temperatura com atraso de semanas |
| B05 | Métricas de servidor | Uso de CPU; requisições, filas |
| B06 | Energia eólica | Geração eólica (ONS); vento de reanálise |
| B07 | Nível do mar | Nível medido; maré astronômica, vento, pressão |

### Frente C: mercado financeiro

Expectativa realista: o retorno do próximo passo é quase imprevisível para qualquer método. Isso torna o mercado um bom
**teste negativo** (ela não deve aceitar entradas espúrias) e um bom teste positivo onde há estrutura conhecida.

| ID | Cenário | Pergunta |
|---|---|---|
| C01 | Retornos diários com várias entradas plausíveis | Ela evita aceitar entradas espúrias? Empata com "prever zero"? |
| C02 | Volatilidade realizada, com volatilidade implícita como entrada | Ela aproveita uma estrutura que se sabe existir? |
| C03 | Câmbio BRL/USD com dólar global e commodities | Há ganho sobre o passeio aleatório? |
| C04 | Curva de juros: variação de spreads | Ela encontra relações entre prazos? |
| C05 | Volume negociado e sazonalidade | Ela aproveita padrões de calendário? |

Fontes preferidas: Banco Central (SGS) e FRED, com a licença de cada série conferida antes do uso.

## 3. Comparadores e métricas

**Comparadores** (todos online e causais, usando só o passado):
- ingênuo (último valor) e sazonal ingênuo (valor de uma estação atrás);
- "prever zero" (para retornos financeiros);
- regressão linear online com defasagens do alvo e das entradas (RLS com esquecimento);
- SARIMAX ajustado por série, quando o custo permitir (não é online; serve de referência forte).

**Métricas de previsão:** MSE e MAE; MSE relativo ao ingênuo e ao linear online; cobertura do intervalo de 90%.

**Métricas de estrutura** (Frente A, onde a verdade é conhecida): entradas verdadeiras aceitas, entradas falsas aceitas,
tempo até a detecção, tempo até a remoção depois de uma mudança de regime.

**Métricas de custo:** operações por passo (média e máximo, contadas pela própria biblioteca) e tempo real por passo.

## 4. Registro de execuções

`runs/REGISTRO.csv`, uma linha por execução, nunca apagada:

`id, data, cenario, frente, commit, versao_lebre, sementes, n_series, criterio, resultado, resumo, notas`

- `resultado`: `atende`, `nao_atende`, `inconclusivo` ou `abortado`, sempre em relação ao critério declarado antes.
- Os detalhes de cada execução ficam em `runs/<id>/` (configuração, métricas por série, eventos da LEBRE).

## 5. Fases

1. **Fase 0, estrutura** (esta): repositório, código comum, registro, teste do código comum.
2. **Fase 1, Frente A:** sintéticos, rápidos e sem licença. Primeiro mapa de limites.
3. **Fase 2, Frente B:** domínios reais, um de cada vez, com licença conferida.
4. **Fase 3, Frente C:** mercado financeiro.
5. **Ao fim de cada fase:** atualizar `MAPA.md` (quando usar e quando não usar) e `FALHAS.md` (o que a próxima versão
   precisa resolver).

## 6. Fora de escopo

- Alterar o algoritmo ou ajustar hiperparâmetros da versão congelada (a configuração canônica é a única testada).
- Estratégias de operação no mercado financeiro.
- Previsão de vários passos à frente (a LEBRE prevê um passo).
