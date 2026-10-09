# Validação 5 da v0.53 (M1 rascunho 5 + M2 candidata Q2): regras de escolha, escritas e commitadas antes de baixar qualquer dado

**Data:** 09/10/2026. **Para quê:** confirmar a M1 rascunho 5 (`ALGORITHM_SPEC_DRAFT_M1_r5.md`) com a M2 candidata Q2
(`M2_CANDIDATA_Q2.md`), aprovadas no desenvolvimento ampliado (E16c e E20, LEBRE Lab), em séries que **nenhuma medição
viu**. Usada **uma única vez**. Regras gerais como nas validações 1 a 4: escolha só por metadados, períodos ou listas
declaradas aqui; nada da reserva da v0.53, do desenvolvimento nem das validações 1 a 4 como alvo (entidades novas, ou
períodos que nenhuma medição usou para aquela entidade; entradas seguem a construção das famílias análogas, como antes);
licenças conferidas antes (FRED: DEXKOUS, DEXMXUS, DEXSZUS, DEXNOUS e DGS6MO, "Public Domain: Citation Requested",
conferidas em 09/10; as demais fontes já conferidas); congelamento com SHA-256 antes da medição; substituição só pela
reserva da família, na ordem.

| Família | Análoga a | Regra de escolha |
|---|---|---|
| Z-B03 | B03 (F6) | UCI *Beijing Multi-Site Air Quality* (CC BY 4.0), mar/2013 a fev/2017, **segunda estação em ordem alfabética** dos arquivos (a primeira foi usada na validação 4). Alvos PM2.5, NO2, CO, O3; entradas como em Y-B03. |
| Z-B01 | B01 (solar) | Usinas solares de posição 31 a 36 por capacidade, mesmo filtro, 2024-2025 (mínimo 3, senão a família sai e isso é declarado). |
| Z-B06 | B06 (eólica) | Idem para eólicas, posição 31 a 36. |
| Z-B02 | B02 (carga) | Os 4 subsistemas, **2002-2005** (se o ONS não tiver esses anos, a família sai e isso é declarado). |
| Z-B07 | B07 (maré) | NOAA CO-OPS 2021-2024, mesma construção: 8516945 Kings Point, 8729840 Pensacola, 8652587 Oregon Inlet, 9431647 Port Orford, 8557380 Lewes, 9449880 Friday Harbor (as quatro primeiras eram reservas nunca usadas). Reserva, na ordem: 9419750 Crescent City, 8770570 Sabine Pass. |
| Z-C01 a Z-C03 | C01 a C03 | Câmbios **nunca usados** DEXKOUS (won), DEXMXUS (peso mexicano), DEXSZUS (franco suíço), DEXNOUS (coroa norueguesa), **2000-2009**, mesma construção de W-C01 a W-C03 (entradas: os outros 3 e variações dos juros de 2 e 10 anos). |
| Z-C04 | C04 | Juros DGS1, DGS5, DGS20 em **2000-2009** (período que nenhuma medição usou para eles), mesma construção (entradas: os outros 2 prazos e retornos de DEXKOUS, DEXMXUS, DEXSZUS). |
| Z-C05 | C05 | Variação mensal (%) via SGS, jan/2001 a dez/2025: 11427 e 4467 (núcleos do IPCA, reservas não usadas da validação 4), 1640 (comunicação), 10843 (bens duráveis). Reserva: 1638 (vestuário; reserva não usada como alvo nas validações anteriores). Conferência numérica (>= 290 meses, correlação > 0,3 com o IPCA) e mínimo 3, como antes; nomes conferidos depois. |
| Z-CURTAS | séries curtas | Primeiros 360 passos de cada série acima, mais Z-C05 inteira; mesma exclusão por falta de alvo. |

## Critérios (fixados antes)

1. **F6 (fronteira)** em Z-B03 e Z-B07 (análogas às famílias em que a v0.52 estava abaixo da fronteira no E14): custo médio
   da v0.53 <= 2,5 × v0.52 e erro (média geométrica ÷ comparador linear online completo) <= 1,05 × o menor erro entre as 8
   variantes do E14 **recalculadas nessas famílias** com custo <= o da v0.53.
2. **Critérios da M2** (régua por decidibilidade com o adendo 3 de 09/10/2026) com M1 r5 + M2 Q2 em todas as famílias Z,
   **Z-C05 incluída**; passo de avaliação com previsão não finita = falha.
3. **Custo** reportado (o teto da v0.53 como um todo é decidido no pré-registro final).

**Código:** cópia fixa do protótipo (git worktree) no commit `bca5dac`. Sementes no plano da medição.
**Regra:** a v0.53 (M1 r5 + M2 Q2) é confirmada se atender a 1 e 2; se não, falhas declaradas, nada ajustado.
