# Base de validação da v0.53 (M2): registro de congelamento

**Data:** 08/10/2026. Regras em `VALIDACAO_PLANO.md` (commit `714ba5b`, antes de qualquer download); módulos em
`scenarios/V/` e `lab/validacao.py` (commit `b729586`, antes do download). Montagem feita só com metadados (tamanho,
fração de alvo observado, período), **sem nenhuma previsão**.

**Manifesto:** `dados/VALIDACAO_SHA256.tsv` (SHA-256 do manifesto: `c2461a7a7a901c1eb591e015cbfd464ca9fa4201a4adaf58ea8df9c17c49fea2`): 93 arquivos novos e 18 compartilhados
com o desenvolvimento (FRED, tabela das usinas, séries 1, 433 e 4390 do SGS). Nenhum arquivo do desenvolvimento mudou
(conferido contra `dados/MANIFESTO_SHA256.tsv`).

## Séries (45)

| Família | Séries | Passos | Observações |
|---|---|---|---|
| VB01 | Açú III 230 kV, Serra do Mel C, Paracatu, Pirapora 2, Ciranda, Rio Alto | 17.544 | Açú III com 95,9% de alvo observado; demais 100%. |
| VB02 | Sudeste, Sul, Nordeste, Norte, 2018-2021 | 35.064 | Inclui 2020 (pandemia), como fato do período. |
| VB06 | Oitis, Ourolândia II, Rio do Vento Expansão, Laranjeiras, Rio do Vento, Serra do Seridó | 17.544 | 100%. |
| VB07 | Baltimore, St. Petersburg, Grand Isle, San Francisco, Seattle, La Jolla | 35.064 | Nenhuma estação de reserva foi necessária; San Francisco com 85,9% de alvo observado. |
| VC01-VC03 | dólar/real, euro/dólar, iene/dólar, WTI, 2000-2009 | 2.609 | 84% (WTI) a 96%. |
| VC04 | juros de 3 meses, 2 e 10 anos, 2000-2009 | 2.609 | 95,8%. |
| VC05 | IPCA-15 (7478), alimentação e bebidas (1635), serviços (10844), preços monitorados (4449), 2001-2025 | 300 | Os 4 passaram na conferência numérica (300 meses; correlação com o IPCA 0,86, 0,69, 0,40 e 0,72); reservas não usadas. Nomes de 4449 e 10844 conferidos no portal de dados abertos do BCB; 7478 e 1635 só em fontes secundárias (mantidos pela regra do plano). |
| VCURTAS | primeiros 360 passos de cada série acima, mais VC05 inteira | 300-360 | Regra de exclusão por falta de alvo aplicada na medição. |

Nenhuma série é do banco de desenvolvimento nem da reserva da v0.53 (`lab/reserva.py` checado na montagem). A base é
usada **uma única vez** para a M2 da v0.53.
