# Diagnóstico E10 de F6: fronteira precisão × custo do especialista (só descrição, nenhuma escolha): plano

**Data:** 08/10/2026. **Decisão do responsável pelo projeto:** a v0.53 não fecha com débito técnico; F6 (B03) precisa
ser resolvida na v0.53. **Por quê este diagnóstico:** E9 mostrou que a vantagem do comparador linear vem da estrutura
conjunta de defasagens. Antes de redesenhar a M1, medir quanto de precisão cada forma de memória conjunta dá e a que custo.

**Variantes (RLS, λ = 0,999, δ = 100), nas 4 séries de B03:**
- AR2+0: 1, alvo defasado 1 e 2, todas as entradas no instante t (11 variáveis);
- AR2+B3: 1, alvo defasado 1 e 2, as 3 entradas de maior correlação no aquecimento resumidas nas bandas da v0.52
  (instante t, defasagem 1, média de 2-3, média de 4-7, média de 8-15) (18 variáveis);
- AR2+B8: o mesmo com as 8 entradas (43 variáveis);
- COMPLETO: o comparador do Lab (75 variáveis).

Cada uma com atualização a cada passo e a cada 8 passos (EVERY da v0.52). **Medido:** MSE ÷ MSE do COMPLETO (atualizado a
cada passo) e ÷ v0.52; custo em FP por passo pela regra da v0.52 (RLS com k variáveis: 6k² + 4k por atualização; previsão
2k; montagem das bandas por entrada ~2 por banda).
