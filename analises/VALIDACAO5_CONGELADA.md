# Validação 5 da v0.53 (M1 r5 + M2 Q2): registro de congelamento

**Data:** 09/10/2026. Regras em `VALIDACAO5_PLANO.md` (commit `a62ee3a`, antes de qualquer download) e adendo 1 (commit
`d3e4dff`: as moedas escolhidas estavam na reserva da v0.53; a trava barrou antes de qualquer download; trocadas por
DEXSFUS, DEXTAUS, DEXINUS em 2000-2009 e DEXUSNZ). Módulos em `scenarios/Z/` e `lab/validacao5.py` (commit `659c4c4`);
correção só de download no leitor do SGS (commit `d4dd8a4`: uma página de erro HTML do BCB tinha ficado no cache); licença
do DEXUSNZ registrada (commit `9f5f752`). Montagem só com metadados, **sem nenhuma previsão**. Manifesto
`dados/VALIDACAO5_SHA256.tsv` (115 arquivos lidos na montagem: 89 novos, 26 compartilhados com hash idêntico ao dos manifestos
anteriores; SHA-256 do manifesto `bcc6db64f160e683a91211ca1abfbf5f80b0a3e0b51c8ad4e8ae255ae06313d0`). Os 587 arquivos dos
manifestos do desenvolvimento e das validações 1 a 4 foram conferidos: nenhum mudou.

Nota: os arquivos do SGS dos códigos 11427 e 4467 foram baixados em 08/10, quando o script de montagem da validação 4
imprimiu a conferência numérica das reservas (só a correlação com o IPCA); não entraram no manifesto da validação 4 nem em
nenhuma medição.

## Séries (39)

| Família | Séries | Passos | Observações |
|---|---|---|---|
| Z-B03 | Changping (segunda estação em ordem alfabética): PM2.5, NO2, CO, O3 | 35.064 | 95,7% a 98,3% do alvo. |
| Z-B01 | Sol do Piauí, Pitombeira, Conj. BJL, Assú V, Flor de Mandacaru (posições 31-35; só 5 a partir da 31ª) | 17.544 | 97,9% a 100%; mínimo 3, a família fica. |
| Z-B06 | Pedra Branca, Oeste Seridó, Arizona, União dos Ventos, São Clemente, Chapada III | 17.544 | 100%. |
| Z-B02 | Sudeste, Sul, Nordeste, Norte, 2002-2005 | 35.064 | 100%; o ONS tem esses anos. |
| Z-B07 | Kings Point, Pensacola, Oregon Inlet Marina, Port Orford, Lewes, Friday Harbor | 35.064 | 100%; nenhuma reserva usada. |
| Z-C01 a Z-C03 | rand, dólar de Taiwan, rúpia, dólar neozelandês, 2000-2009 | 2.609 | ~96,4%. |
| Z-C04 | juros de 1, 5 e 20 anos, 2000-2009 | 2.609 | 95,8%. |
| Z-C05 | 11427 e 4467 (núcleos do IPCA), 10843 (bens duráveis), 2001-2025 | 300 | Conferência numérica: 1640 (0,19) e a reserva 1638 (0,17) reprovam; 3 códigos, pelo mínimo de 3. Nomes a conferir depois. |
| Z-CURTAS | primeiros 360 passos de cada série acima, mais Z-C05 inteira | 300-360 | |

Nada da reserva da v0.53, do desenvolvimento ou das validações 1 a 4 como alvo. Usada uma única vez, para a v0.53 com M1
rascunho 5 e M2 candidata Q2.
