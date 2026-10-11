# Validação 6 (v0.54, M5a rascunho 2): registro de congelamento

**Data:** 11/10/2026. Regras em `VALIDACAO6_PLANO.md` (commit `ba1a01e`, antes de qualquer download). Módulos em
`scenarios/U/` e `lab/validacao6.py` (commit `8cf6146`); montagem por `analises/montar_validacao6.py` (commit `eeaac57`), só
com metadados, **sem nenhuma previsão**. Manifesto `dados/VALIDACAO6_SHA256.tsv` (77 arquivos lidos na montagem: 74 novos,
3 compartilhados com hash idêntico ao dos manifestos anteriores; SHA-256 do manifesto
`23750f51b008acb99913ad5ae98676ec8b9cda7b5019650d7c59923dc8dae9d3`). Os arquivos dos manifestos do desenvolvimento e das
validações 1 a 5 foram conferidos: nenhum mudou. Detalhe por série em `validacao6_montagem.json`.

## Séries (24 reais + 50 sintéticas)

| Família | Séries | Passos | Observações |
|---|---|---|---|
| U-A01 | 30 sintéticas (d = 10, 20, 50; sementes 20261200 a 20261229) | 20.000 | Gerador de A01. |
| U-A05 | 20 sintéticas (sementes 20261230 a 20261249) | 30.000 | Gerador de A05. |
| U-B02 | Sudeste, Sul, Nordeste, Norte, 2000-2001 | 17.544 | 99,99% do alvo; ciclo 24 + 168. |
| U-B03 | Dingling (terceira estação em ordem alfabética): PM2.5, NO2, CO, O3 | 35.064 | 94,3% a 97,8% do alvo; ciclo 24 + 168. |
| U-B06 | Paranatama, Faísa, Baixa do Feijão, Trairí, Chapada I, Delfina (posições 37 a 42; nenhuma da reserva da v0.54) | 17.544 | 100%; ciclo 24. |
| U-B07 | Crescent City, Clearwater Beach, Virginia Key, San Diego, Anchorage, Honolulu | 35.064 | 96,6% a 100%. **Sabine Pass (8770570) não tem nível de maré horário em 2021**: trocada pela primeira reserva, Clearwater Beach, pela regra do plano. |

Nada das reservas das avaliações finais da v0.53 e da v0.54, do desenvolvimento ou das validações 1 a 5 como alvo. Usada
uma única vez, para a M5a (rascunho 2).
