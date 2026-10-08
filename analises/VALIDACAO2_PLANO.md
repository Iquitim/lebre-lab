# Validação 2 da v0.53 (M2): regras de escolha, escritas e commitadas antes de baixar qualquer dado

**Data:** 08/10/2026. **Para quê:** confirmar a candidata D (`M2_CANDIDATA_D.md`, lebre-research `442db78`) com a régua por
decidibilidade, em séries que **nenhuma medição viu**. Usada **uma única vez**. Mesmas regras gerais de
`VALIDACAO_PLANO.md`: escolha só por metadados, períodos ou listas declaradas aqui; nada da reserva da v0.53; nada do
desenvolvimento nem da validação 1; congelamento com SHA-256 antes da medição; substituição só pela reserva da própria
família, na ordem.

| Família | Análoga a | Regra de escolha |
|---|---|---|
| W-B01 | B01 (solar) | Usinas solares de posição 13 a 18 por capacidade, mesmo filtro de B01, 2024-2025. Se houver menos de 18 que passem no filtro, usam-se as que houver a partir da 13ª (mínimo 3; abaixo disso a família sai e isso é declarado). |
| W-B06 | B06 (eólica) | Idem para eólicas. |
| W-B02 | B02 (carga) | Os 4 subsistemas, **2014-2017**, mesma construção. |
| W-B07 | B07 (maré meteorológica) | NOAA CO-OPS 2021-2024, mesma construção; coordenadas pela API de metadados da NOAA. Estações: 8454000 Providence, 8658120 Wilmington, 8452660 Newport, 8545240 Philadelphia, 9418767 North Spit, 9435380 South Beach. Reserva, na ordem: 8516945 Kings Point, 8729840 Pensacola. |
| W-C01 | C01 (retornos, negativa) | Retorno log diário (%) de 4 câmbios do Fed H.10 **fora da reserva e nunca usados**: DEXINUS (rúpia), DEXSIUS (dólar de Singapura), DEXTHUS (baht), DEXDNUS (coroa dinamarquesa), 2010-2025. Entradas com 1 dia de atraso: os outros 3 e as variações dos juros de 2 e 10 anos (como em C01). Referência zero. |
| W-C02 | C02 (volatilidade) | |retorno| dos mesmos 4, mesmas entradas em valor absoluto. |
| W-C03 | C03 (níveis, negativa) | Níveis dos mesmos 4; entradas: níveis dos outros 3 e juros de 2 e 10 anos. |
| W-C04 | C04 (juros, negativa) | Variação diária dos juros do Fed H.15 de prazos **nunca usados**: DGS1, DGS5, DGS30, 2010-2025. Entradas com 1 dia de atraso: os outros 2 prazos e retornos dos câmbios de W-C01 (os 3 primeiros). Referência zero. |
| W-C05 | C05 (inflação mensal curta) | Variação mensal (%) de grupos do IPCA via SGS, jan/2001 a dez/2025: 1636 (habitação), 1639 (transportes), 1641 (saúde e cuidados pessoais), 1643 (educação). Reserva, na ordem: 1638 (vestuário), 1642 (despesas pessoais). Mesma conferência numérica de VC05 (>= 290 meses, correlação > 0,3 com o IPCA); nomes conferidos depois, como em VC05. Entradas como em VC05. |
| W-CURTAS | séries curtas | Primeiros 360 passos de cada série acima, mais W-C05 inteira; mesma exclusão por falta de alvo. |

**Licenças:** Fed H.10 e H.15 são de domínio público (mesma fonte das séries já usadas pelo Lab); a lista de séries
liberadas em `lab/fontes.py` é ampliada só com as séries acima, com a origem registrada em `dados/FONTES.md`. NOAA,
ONS, Open-Meteo e SGS como antes.

**Régua:** a de `M2_CANDIDATA_D.md` (decidibilidade). Correspondência das famílias para os critérios 4 e 5 e 6 como nas
análogas. Semente do bootstrap da classificação e da medição fixada no plano da medição.

## Adendo 1 (08/10/2026, na montagem, antes de qualquer medição)

A conferência numérica de W-C05 (só dados: meses observados e correlação com o IPCA) aprovou 3 dos 6 códigos: 1636
(correlação 0,42), 1639 (0,73) e 1642 (0,32); reprovou 1641 (0,29), 1643 (0,19) e 1638 (0,17). O plano não previa menos
de 4. Regra acrescentada, que depende só dessa conferência: **W-C05 segue com as 3 séries aprovadas** (mínimo 3; abaixo
disso a família sairia). Nenhum código novo foi acrescentado.
