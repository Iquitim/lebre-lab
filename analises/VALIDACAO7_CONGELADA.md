# Validação 7: congelamento (antes de qualquer previsão)

**Data:** 11/10/2026. Regras em `VALIDACAO7_PLANO.md` (commit `1b78d47`, antes de qualquer download). Montagem:
`analises/montar_validacao7.py` (só metadados, nenhuma previsão); resumo em `analises/validacao7_montagem.json`.

- **Manifesto:** `dados/VALIDACAO7_SHA256.tsv`, 8 arquivos (6 novos, 2 compartilhados com hash idêntico ao de manifestos
  anteriores); SHA-256 do manifesto `e0ef5139962fb86a0b9659c0864466b3f39f6140d22aa4d09531056c10c8b2e0`. Nenhum arquivo de
  manifesto anterior mudou.
- **T-B03:** estação Dongsi (quarta em ordem alfabética), alvos PM2.5, NO2, CO e O3; 35.064 passos; cobertura do alvo
  de 0,909 a 0,981.
- **T-B06:** 6 eólicas (Itarema V, Cumaru, Serrote A, Umari, Caetité Norte, GPEXPAN), 17.544 passos, cobertura de
  0,970 a 1,000. Nenhuma aparece em uso anterior no Lab, e nenhuma é da reserva da v0.54 (recusadas ao carregar).
- **Sintéticas:** T-A01 (30), T-A05 (20), T-A07 (20), T-A02 (20), com as sementes do plano.

Nenhuma substituição foi necessária.
