# Validação 2 da v0.53 (M2): registro de congelamento

**Data:** 08/10/2026. Regras em `VALIDACAO2_PLANO.md` (commit `bd71fcb`, antes de qualquer download; adendo 1 em
`e545088`, antes de qualquer medição); módulos em `scenarios/W/` e `lab/validacao2.py` (commit `f2992ed`). Montagem
só com metadados, **sem nenhuma previsão**. Manifesto `dados/VALIDACAO2_SHA256.tsv` (SHA-256 `462238216c70c8c8e0fe9727339ed2434526d01fc833f0fb4ec0bdece68d5392`). Nenhum arquivo do
desenvolvimento nem da validação 1 mudou.

## Séries (40; a primeira versão deste registro dizia 45, erro de contagem corrigido)

| Família | Séries | Passos | Observações |
|---|---|---|---|
| W-B01 | Nova Olinda, Castilho, Ituverava, Boa Hora, Abaiara 230 kV, Brígida (posições 13-18) | 17.544 | Boa Hora 96,4% e Abaiara 95,9% de alvo observado. |
| W-B06 | Serra do Mel B, Santo Agostinho, Paulino Neves, Novo Horizonte, Serra da Babilônia, Umburanas | 17.544 | 100%. |
| W-B02 | Sudeste, Sul, Nordeste, Norte, 2014-2017 | 35.064 | 99,9%. |
| W-B07 | Providence, Wilmington, Newport, Philadelphia, North Spit, South Beach | 35.064 | 100%; nenhuma reserva usada. |
| W-C01 a W-C03 | rúpia, dólar de Singapura, baht, coroa dinamarquesa, 2010-2025 | 4.174 | ~95,8%. |
| W-C04 | juros de 1, 5 e 30 anos, 2010-2025 | 4.174 | 95,8%. |
| W-C05 | IPCA habitação (1636), transportes (1639), despesas pessoais (1642), 2001-2025 | 300 | Adendo 1: 3 de 6 códigos passaram na conferência numérica. Nomes confirmados só por fonte secundária. |
| W-CURTAS | primeiros 360 passos de cada série acima, mais W-C05 inteira | 300-360 | |

Nada da reserva da v0.53 (`lab/reserva.py` checado na montagem), do desenvolvimento ou da validação 1. Usada uma única
vez, para a candidata D.
