# Validação 4 da v0.53 (M1 com M2): regras de escolha, escritas e commitadas antes de baixar qualquer dado

**Data:** 08/10/2026. **Para quê:** confirmar a M1 rascunho 2 (`ALGORITHM_SPEC_DRAFT_M1_r2.md`, com a M2 candidata P) em
séries que **nenhuma medição viu**, incluindo uma família análoga a B03 (F6) com dados novos. Usada **uma única vez**.
Regras gerais como nas validações 1 a 3 (escolha só por metadados, períodos ou listas declaradas aqui; nada da reserva da
v0.53, do desenvolvimento nem das validações 1 a 3 como **dado**: entidades novas, ou períodos que nenhuma medição usou;
licença conferida antes; congelamento com SHA-256 antes da medição; substituição só pela reserva da família, na ordem).

| Família | Análoga a | Regra de escolha |
|---|---|---|
| Y-B03 | B03 (F6) | UCI *Beijing Multi-Site Air Quality* (Chen, 2017, doi:10.24432/C5RK5G; CC BY 4.0 conferida), horária, mar/2013 a fev/2017. Estação: a **primeira em ordem alfabética** dos arquivos. Alvos: PM2.5, NO2, CO, O3. Entradas no mesmo instante (como em B03): os 5 outros poluentes medidos (dos 6) e TEMP, PRES, DEWP, RAIN, WSPM. season = 24, season2 = 168. |
| Y-B01 | B01 (solar) | Usinas solares de posição 25 a 30 por capacidade, mesmo filtro, 2024-2025 (mínimo 3). |
| Y-B06 | B06 (eólica) | Idem para eólicas, posição 25 a 30. |
| Y-B02 | B02 (carga) | Os 4 subsistemas, **2006-2009** (se o ONS não tiver esses anos, a família sai e isso é declarado). |
| Y-B07 | B07 (maré) | NOAA 2021-2024: 8410140 Eastport, 8413320 Bar Harbor, 8418150 Portland, 8531680 Sandy Hook, 8575512 Annapolis, 9415020 Point Reyes. Reserva: 8652587 Oregon Inlet, 9431647 Port Orford. |
| Y-C01 a Y-C03 | C01 a C03 | Câmbios DEXJPUS, DEXDNUS, DEXSIUS, DEXTHUS no **período 1990-1999** (nenhuma medição usou esses anos; licenças já conferidas), mesma construção de W-C01 a W-C03. |
| Y-C04 | C04 | Juros DGS1, DGS5, DGS30 em **1990-1999**, mesma construção de W-C04 (entradas: os outros 2 prazos e retornos de DEXJPUS, DEXDNUS, DEXSIUS). |
| Y-C05 | C05 | Núcleos do IPCA via SGS, jan/2001 a dez/2025: 4466, 11426, 16121, 16122. Reserva: 11427, 4467. Conferência numérica e mínimo 3 como antes. |
| Y-CURTAS | séries curtas | Primeiros 360 passos de cada série acima, mais Y-C05 inteira. |

## Critérios (fixados antes)

1. **F6 em Y-B03 (fronteira, mesma regra do rascunho 1 da M1):** custo médio da v0.53 <= 2,5 vezes o da v0.52 em Y-B03 e
   erro (média geométrica ÷ comparador linear online completo) <= 1,05 × o menor erro entre as variantes do E10
   **recalculadas em Y-B03** (AR2+0, AR2+B3, AR2+B-todas, completo; a cada passo e a cada 8 passos; custo pela mesma
   fórmula com o d de Y-B03) com custo <= o da v0.53.
2. Critérios da M2 (régua por decidibilidade) em todas as famílias Y com M1 + M2, **Y-C05 incluída**.
3. Custo reportado (o teto da v0.53 como um todo é decidido no pré-registro final).

Sementes no plano da medição. **Regra:** a M1 é confirmada se atender a 1 e 2; se não, falhas declaradas, nada ajustado.
