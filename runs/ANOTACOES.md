# Anotações sobre execuções registradas

O registro (`REGISTRO.csv`) nunca é editado. Problemas descobertos depois de uma execução ficam anotados aqui.

## 2026-10-04: comparador linear online divergiu em séries longas

- **Execuções afetadas:** `20261004-175618_A05`, `20261004-175718_A06`, `20261004-175818_A07` (30 mil passos) e
  `20261004-180351_A12` (200 mil passos).
- **O que aconteceu:** a matriz P do RLS acumulou assimetria por arredondamento (cerca de 8 vezes a cada 2 mil passos),
  deixou de ser positiva definida perto de 25 mil passos e o comparador divergiu (MSE de 200 a 2e10).
- **Consequência:** nessas execuções, o MSE relativo ao linear online (`mse_rel_linear_online*`) é inválido. Em A06 e
  A07, a parte do critério "MSE relativo ao linear online <= 1,10" foi satisfeita só por causa da divergência e não
  conta. As métricas de estrutura e o MSE da própria LEBRE não dependem do comparador e continuam válidos. O critério do
  A12 não usa o comparador; o resultado "nao_atende" dele continua valendo.
- **Execuções de 20 mil passos não foram afetadas:** recalculado com o comparador corrigido em 6 séries (A01 com d = 10
  e d = 50, A04, A08, A09, A11), o MSE ficou idêntico ao registrado.
- **Correção:** simetrização de P a cada passo e reinício de segurança (`lab/baselines.py`), com teste de regressão de
  40 mil passos. A05, A06, A07 e A12 foram rodados de novo como execuções novas, com nota citando as originais.

## 2026-10-04: execução de D03 abortada e não registrada

- **O que aconteceu:** a primeira execução de D03 (19:04 a 19:07, commit `b34e037`) rodou as 26 séries e quebrou no
  resumo (`KeyError: 'mse_rel_sazonal_ingenuo'`): o cenário mistura séries com e sem sazonal ingênuo (as marés de B07
  não declaram ciclo), e o resumo supunha os mesmos comparadores em todas.
- **Por que não está em REGISTRO.csv:** o executor ainda não registrava execuções que quebravam. Esta anotação cumpre
  a regra 3 do PLANO no lugar da linha que faltou.
- **Correções:** o resumo aceita comparadores diferentes entre séries (com teste de regressão), e o executor agora
  registra qualquer execução que quebre como `abortado`. D03 foi rodado de novo, sem mudança no cenário.

## 08/10/2026: medição da M2, rascunho 2, família CURTAS abortada

`analises/m2_dev_r2.py CURTAS` abortou (IndexError no quantil): a série B01 "Conj. Arinos 2 500 kV" não tem alvo
observado nos primeiros 360 passos. Corrigido por regra de disponibilidade declarada no adendo 1 de
`analises/M2_DEV_R2_PLANO.md` (exclui séries curtas com menos de 144 de 288 alvos observados na janela); só essa série é
afetada. CURTAS rodada de novo depois do commit da correção.

## 08/10/2026: medição da M2, rascunho 3, interrompida de propósito

`analises/m2_dev_r3.py` foi interrompido (processos parados) depois que a configuração única S já falhava nos critérios
1, 2 e 7 em várias famílias; pela regra do plano (escolha só se atender a todos) as famílias restantes não podiam mudar o
resultado. Medidas: C05, CURTAS, B01, B02, C01-C04. Não medidas: A01-A12, B03, B06, B07. Arquivos parciais de logs não
foram versionados. Resultado em `analises/M2_DEV_R3_RESULTADO.md`.

## 08/10/2026: medição da M2, rascunho 5, interrompida de propósito

`analises/m2_dev_r5.py` interrompido depois que C05 já falhava o critério 2 (regra decidida); B01 foi esperado de
propósito para saber se o compartilhamento resolvia a série Arinos (resolveu). Medidas: C05, CURTAS, B01, C01-C04.

## 08/10/2026: diagnóstico E5 da M2, processos reiniciados para manter o registro de commit exato

Enquanto o E5 rodava (protótipo `85da1ff` carregado em memória), o protótipo recebeu um acréscimo (oráculo de Jeffreys)
e foi commitado em `4c8f102`. As 32 famílias já gravadas registraram `85da1ff` corretamente (nenhuma abortou; nenhuma
começou com o protótipo sujo). As famílias ainda por começar registrariam `4c8f102` executando o código antigo; para que o
registro seja exato, os 3 processos restantes foram parados e as 11 famílias que faltavam (A02, A04-A12, B07) rodadas de
novo a partir de `4c8f102`, em que o caminho do oráculo `switch_mono_exato` é o mesmo (só houve acréscimos).
