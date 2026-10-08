# Diagnóstico E10 de F6: fronteira precisão × custo (B03)

MSE ÷ MSE do comparador linear completo atualizado a cada passo. Custo em FP por passo (regra da v0.52) do especialista sozinho.

| Série | v0.52 | AR2+0/1 | AR2+0/8 | AR2+B3/1 | AR2+B3/8 | AR2+B8/1 | AR2+B8/8 | COMPLETO/1 | COMPLETO/8 |
|---|---|---|---|---|---|---|---|---|---|
| CO(GT) | 1.716 | 1.777 | 2.138 | 1.225 | 1.295 | 1.080 | 1.205 | 1.000 | 1.195 |
| NOx(GT) | 1.496 | 1.505 | 1.834 | 1.166 | 1.482 | 0.992 | 1.277 | 1.000 | 1.312 |
| NO2(GT) | 1.308 | 1.397 | 1.538 | 1.093 | 1.246 | 1.037 | 1.152 | 1.000 | 1.170 |
| C6H6(GT) | 5.533 | 2.296 | 3.873 | 2.184 | 2.564 | 1.323 | 1.622 | 1.000 | 1.287 |
| **geo** | **2.076** | **1.711** | **2.198** | **1.359** | **1.574** | **1.101** | **1.302** | **1.000** | **1.239** |
| FP/passo | - | 872 | 198 | 2082 | 318 | 11432 | 1574 | 34200 | 4406 |

## Leitura

Custo da v0.52 em B03 (medido): ~650-760 FP por passo. **Chegar a 1,05 do comparador exige um especialista de 11 mil a
34 mil FP por passo** (15 a 50 vezes a própria v0.52): AR2+B8 a cada passo (1,10) ou o comparador completo (1,00). Com
custo comparável ao da v0.52, porém, RLS mais simples já a superam com folga: AR2+B3 a cada 8 passos (318 FP) fica em 1,57
e AR2+B8 a cada 8 passos (1.574 FP) em 1,30, contra 2,08 da v0.52. Leitura: F6 é **real** (com o mesmo orçamento de
cálculo, uma regressão conjunta de defasagens aprende melhor que o modelo base da v0.52 nesses dados), mas o critério da
nota de desenho (1,05 do comparador de 75 variáveis atualizado a cada passo) mede contra um modelo 45 vezes mais caro.
