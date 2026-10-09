# Validação 4 da v0.53 (M1 com M2): registro de congelamento

**Data:** 08/10/2026. Regras em `VALIDACAO4_PLANO.md` (commit `6e923a5`, antes de qualquer download); módulos em
`scenarios/Y/` e `lab/validacao4.py` (commit `80e800e`), com uma correção só de leitura do arquivo da UCI (commit
`ba50dbb`: os CSVs das estações vêm num zip interno; o leitor pegava os CSVs do zip externo e falhava antes de montar
qualquer série). Montagem só com metadados, **sem nenhuma previsão**. Manifesto `dados/VALIDACAO4_SHA256.tsv` (113
arquivos lidos na montagem: 93 novos, 20 compartilhados com hash idêntico ao dos manifestos anteriores; SHA-256 do
manifesto `83f6a6c1353f574e61e9a0686c6a4d31846e4fa38bcbffbbdc183b639e33443e`). Os 474 arquivos dos manifestos do
desenvolvimento e das validações 1 a 3 foram conferidos: nenhum mudou.

Os compartilhados são as séries completas do FRED (das quais só 1990-1999 entra aqui, período que nenhuma medição usou),
as séries do SGS usadas na conferência numérica de Y-C05 e os metadados do ONS (lista de arquivos e cadastro de usinas).

## Séries (43)

| Família | Séries | Passos | Observações |
|---|---|---|---|
| Y-B03 | Aotizhongxin (primeira estação em ordem alfabética): PM2.5, NO2, CO, O3 | 35.064 | 94,9% a 97,4% do alvo. |
| Y-B01 | Sol do Futuro, Dracena, Horizonte, Lapa, Bom Jesus, São Pedro (posições 25-30) | 17.544 | 100%. |
| Y-B06 | Gentio do Ouro I, Ventos da Bahia, Lagoa do Barro I, Igaporã II, Jerusalém, Monte do Ronca | 17.544 | 99,6% a 100%. |
| Y-B02 | Sudeste, Sul, Nordeste, Norte, 2006-2009 | 35.064 | 100%; o ONS tem esses anos, a família fica. |
| Y-B07 | Eastport, Bar Harbor, Portland, Sandy Hook, Annapolis, Point Reyes | 35.064 | 100%; nenhuma reserva usada. |
| Y-C01 a Y-C03 | iene, coroa dinamarquesa, dólar de Singapura, baht, 1990-1999 | 2.610 | 94,2% a 96,4%. |
| Y-C04 | juros de 1, 5 e 30 anos, 1990-1999 | 2.610 | 95,9%. |
| Y-C05 | núcleos do IPCA 4466, 11426, 16121, 16122, 2001-2025 | 300 | Conferência numérica: os 4 primários passam (correlação com o IPCA 0,655; 0,832; 0,796; 0,868); nenhuma reserva usada. |
| Y-CURTAS | primeiros 360 passos de cada série acima, mais Y-C05 inteira | 300-360 | |

Nada da reserva da v0.53, do desenvolvimento ou das validações 1 a 3 como dado. Usada uma única vez, para a M1 rascunho 2
com a M2 candidata P.

**Errata (09/10/2026):** as famílias B01, B02 e B06 (e as curtas delas) foram montadas com `season=30` em vez de 24; ver `ERRATA_SEASON_VALIDACOES_4_5.md`.
