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
