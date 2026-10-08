# Validação 3 da v0.53 (M2): registro de congelamento

**Data:** 08/10/2026. Regras em `VALIDACAO3_PLANO.md` (commit `e12ffd7`, antes de qualquer download); licenças das 7
séries novas do FRED conferidas antes do download (todas "Public Domain: Citation Requested"; nenhuma reserva usada);
módulos em `scenarios/X/` e `lab/validacao3.py` (commit `212f021`). Montagem só com metadados, **sem nenhuma
previsão**. Manifesto `dados/VALIDACAO3_SHA256.tsv` (SHA-256 `8576e54b847fa696ba69e6dae8c013ef2e10b5606de2f6cf7dd987666a9fe9e2`). Nenhum arquivo do desenvolvimento nem das
validações 1 e 2 mudou.

## Séries (41)

| Família | Séries | Passos | Observações |
|---|---|---|---|
| X-B01 | Guaimbê, Francisco Sá, Sertão Solar Barreiras, Pedranópolis, Araxá, Floresta (posições 19-24) | 17.544 | 100%. |
| X-B06 | Babilônia Sul, Morro do Chapéu Sul II, Folha Larga, Tucano, Lagoa dos Barros, Cutia | 17.544 | 100%. |
| X-B02 | Sudeste, Sul, Nordeste, Norte, 2010-2013 | 35.064 | 99,9%. |
| X-B07 | New London, Woods Hole, Sewells Point, Dauphin Island, Los Angeles, Toke Point | 35.064 | 100%; nenhuma reserva usada. |
| X-C01 a X-C03 | ringgit, dólar de Taiwan, rúpia do Sri Lanka, rand, 2010-2025 | 4.174 | ~95,8%. |
| X-C04 | juros de 3, 7 e 20 anos, 2010-2025 | 4.174 | 95,8%. |
| X-C05 | IPCA comercializáveis (4447), não comercializáveis (4448), bens não duráveis (10841), artigos de residência (1637), 2001-2025 | 300 | Conferência numérica: 10842 reprovado (correlação 0,28), substituído pela primeira reserva (1637, 0,53), como manda a regra. Nomes de 4447 e 10841 vistos no portal de dados abertos do BCB; 4448 e 1637 só em fontes secundárias. |
| X-CURTAS | primeiros 360 passos de cada série acima, mais X-C05 inteira | 300-360 | |

Nada da reserva da v0.53, do desenvolvimento ou das validações 1 e 2. Usada uma única vez, para a candidata P.
