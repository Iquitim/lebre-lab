# Base de validação da v0.53 (M2): regras de escolha, escritas e commitadas antes de baixar qualquer dado

**Data:** 08/10/2026. **Para quê:** o banco de desenvolvimento do Lab já foi usado em seis medições da M2 (rascunhos 0 a
5) e está "gasto". A base de validação é uma terceira base, entre o desenvolvimento e a reserva final: séries que
**nenhum rascunho viu**, fora da reserva da v0.53. O candidato da M2 (rascunho 6) só vai à reserva final se passar no
desenvolvimento **e** na validação.

**Regras gerais:**

- Escolha só por metadados, períodos ou listas declaradas aqui; nunca por resultados de previsão.
- Nada da reserva da v0.53 (`lab/reserva.py` recusa usinas e câmbio reservados e dados de 2026).
- Nenhuma série do banco de desenvolvimento: entidades novas ou períodos que o Lab não usou.
- Depois do download, os arquivos recebem SHA-256 (`dados/VALIDACAO_SHA256.tsv`) e são congelados com commit **antes**
  de qualquer medição. A base é usada uma única vez para a M2 da v0.53.
- Se uma série prevista não puder ser obtida, entra a próxima da lista de reserva da própria família, na ordem declarada.

## Famílias

| Família | Análoga a | Séries | Regra de escolha |
|---|---|---|---|
| VB01 | B01 (solar) | 6 usinas | As usinas solares de posição 7 a 12 por capacidade, com o mesmo filtro de B01 (coordenadas, >= 95% das horas com geração, fora da reserva), 2024-2025; mesmas entradas de tempo. |
| VB06 | B06 (eólica) | 6 usinas | Idem para eólicas, posições 7 a 12. |
| VB02 | B02 (carga) | 4 subsistemas | Os mesmos 4 subsistemas e capitais, **período 2018-2021** (o desenvolvimento usou 2022-2025; 2026 é reserva). |
| VB07 | B07 (maré meteorológica) | 6 estações | NOAA CO-OPS, 2021-2024, mesma construção de B07, estações fixadas aqui por dispersão geográfica (Atlântico médio, Golfo, Pacífico): 8574680 Baltimore, 8726520 St. Petersburg, 8761724 Grand Isle, 9414290 San Francisco, 9447130 Seattle, 9410230 La Jolla. Reserva, na ordem: 8454000 Providence, 8658120 Wilmington. |
| VC01 | C01 (retornos, negativa) | 4 | Mesmos ativos e entradas, **período 2000-2009** (o desenvolvimento usou 2010-2025). |
| VC02 | C02 (volatilidade) | 4 | Idem, 2000-2009. |
| VC03 | C03 (níveis, negativa) | 4 | Idem, 2000-2009. |
| VC04 | C04 (juros, negativa) | 3 | Idem, 2000-2009. |
| VC05 | C05 (inflação mensal curta) | 4 | Variação mensal (%) de índices do IBGE via SGS do BCB, jan/2001 a dez/2025 (300 meses): IPCA-15 (7478), IPCA alimentação e bebidas (1635), IPCA serviços (10844), IPCA preços monitorados (4449). Entradas com 1 mês de atraso: IPCA cheio (433), variação % do dólar médio do mês (série 1) e Selic acumulada no mês (4390), como em C05. season = 12. Conferência de cada código antes de usar (só dados, não previsão): série mensal com >= 290 meses observados no período e correlação > 0,3 com o IPCA (433). Reserva, na ordem: 11428, 4448 (mesma conferência). Os nomes dos códigos vêm do catálogo do SGS como os conhecemos e serão conferidos na página do SGS; se um nome divergir, o código é mantido se passar na conferência numérica e o nome é corrigido. |
| VCURTAS | família das séries curtas | todas | Os primeiros 360 passos de cada série de VB01, VB02, VB06, VB07 e VC01 a VC04, mais VC05 inteira; mesma regra de exclusão por falta de alvo do adendo 1 de `M2_DEV_R2_PLANO.md`. |

**Sem famílias sintéticas:** novas sementes dos geradores A01 a A12 seriam baratas de gerar mas caras de rodar (séries de
dezenas de milhares de passos), e o risco que a validação cobre é o de dados reais; é uma limitação declarada.

## Critérios na validação (os mesmos do desenvolvimento, por família análoga)

1. VC01, VC03, VC04: limite superior do IC 95% de M2 ÷ referência <= 1,01.
2. VB01, VB02, VB06, VB07, VC02, VC05: limite superior do IC 95% de M2 ÷ v0.52 <= 1,02.
4. VC01, VC04: séries com entrada externa aceita não mais que na v0.52.
5. Acréscimo médio de custo <= 75 FP por passo.
6. Caminho estrutural idêntico ao da v0.52.
7. VCURTAS: limite superior do IC 95% de M2 ÷ melhor(v0.52, referência) <= 1,05.

Bootstrap de blocos pareado, B = 2000, blocos 168 (horárias), 20 (dias úteis), 12 (mensais); em VCURTAS 24, 20, 12.
Semente fixada no plano da medição.
