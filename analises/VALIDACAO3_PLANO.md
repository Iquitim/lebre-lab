# Validação 3 da v0.53 (M2): regras de escolha, escritas e commitadas antes de baixar qualquer dado

**Data:** 08/10/2026. **Para quê:** confirmar a candidata P (`M2_CANDIDATA_P.md`, lebre-research) com a régua por
decidibilidade e o limite de custo de 150 FP por passo, em séries que **nenhuma medição viu**. Usada **uma única vez**.
Mesmas regras gerais de `VALIDACAO_PLANO.md` e `VALIDACAO2_PLANO.md`: escolha só por metadados, períodos ou listas
declaradas aqui; nada da reserva da v0.53, do desenvolvimento nem das validações 1 e 2; licença conferida antes do
download; congelamento com SHA-256 antes da medição; substituição só pela reserva da própria família, na ordem.

| Família | Análoga a | Regra de escolha |
|---|---|---|
| X-B01 | B01 (solar) | Usinas solares de posição 19 a 24 por capacidade, mesmo filtro de B01, 2024-2025 (as que houver a partir da 19ª; mínimo 3, senão a família sai e isso é declarado). |
| X-B06 | B06 (eólica) | Idem para eólicas, posição 19 a 24. |
| X-B02 | B02 (carga) | Os 4 subsistemas, **2010-2013**, mesma construção (se o ONS não tiver esses anos, a família sai e isso é declarado). |
| X-B07 | B07 (maré meteorológica) | NOAA CO-OPS 2021-2024, mesma construção; coordenadas pela API de metadados. Estações: 8461490 New London, 8447930 Woods Hole, 8638610 Sewells Point, 8735180 Dauphin Island, 9410660 Los Angeles, 9440910 Toke Point. Reserva, na ordem: 8516945 Kings Point, 8729840 Pensacola. |
| X-C01 | C01 (retornos, negativa) | Retorno log diário de 4 câmbios do Fed H.10 **fora da reserva e nunca usados**: DEXMAUS (ringgit), DEXTAUS (dólar de Taiwan), DEXSLUS (rúpia do Sri Lanka), DEXSFUS (rand), 2010-2025, mesma construção de W-C01 (entradas: os outros 3 e variações dos juros de 2 e 10 anos). Referência zero. |
| X-C02 | C02 (volatilidade) | |retorno| dos mesmos 4. |
| X-C03 | C03 (níveis, negativa) | Níveis dos mesmos 4. |
| X-C04 | C04 (juros, negativa) | Variação diária dos juros do Fed H.15 de prazos **nunca usados**: DGS3, DGS7, DGS20, 2010-2025; entradas: os outros 2 prazos e retornos de DEXMAUS, DEXTAUS e DEXSLUS. Referência zero. |
| X-C05 | C05 (inflação mensal curta) | Variação mensal (%) de classificações do IPCA via SGS, jan/2001 a dez/2025: 4447 (comercializáveis), 4448 (não comercializáveis), 10841 (bens não duráveis), 10842 (bens semiduráveis). Reserva, na ordem: 1637 (artigos de residência), 1640 (comunicação). Mesma conferência numérica (>= 290 meses, correlação > 0,3 com o IPCA); mínimo 3 (adendo 1 da validação 2). Entradas como em VC05. |
| X-CURTAS | séries curtas | Primeiros 360 passos de cada série acima, mais X-C05 inteira; mesma exclusão por falta de alvo. |

**Licenças:** as 7 séries novas do FRED (DEXMAUS, DEXTAUS, DEXSLUS, DEXSFUS, DGS3, DGS7, DGS20) só entram se a página de
cada uma trouxer a etiqueta "Public Domain: Citation Requested"; uma que não trouxer é trocada pela próxima de uma reserva
declarada aqui: câmbio DEXHKUS, DEXCHUS; juros DGS1MO, DGS6MO (nessa ordem). NOAA, ONS, Open-Meteo e SGS como antes.

**Régua e custo:** a de `M2_CANDIDATA_D.md` (decidibilidade) e critério 5 em 150 FP por passo. Sementes fixadas no plano
da medição.
