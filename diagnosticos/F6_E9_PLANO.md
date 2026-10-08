# Diagnóstico E9 de F6 (só descrição, nenhuma escolha): plano

**Data:** 08/10/2026. **Por quê:** a M1 enxuta (RLS nas 3 entradas no instante t) reduziu o atraso da v0.52 contra o
linear online em B03 só de 2,08 para 1,90 vez (E8). O linear online do Lab usa 1 + 2 defasagens do alvo + 9 defasagens de
cada entrada (instante t e 8 anteriores). Pergunta: de onde vem a vantagem dele em B03?

**Variantes do mesmo RLS (λ = 0,999, δ = 100), nas 4 séries de B03, MSE na janela de avaliação:**
- L0: só as entradas no instante t (com intercepto);
- L0Y: L0 + 2 defasagens do alvo;
- Q8: entradas no instante t e 8 defasagens (sem defasagens do alvo);
- COMPLETO: o comparador do Lab (p = 2, q = 8);
- TOP3: as 3 entradas mais correlacionadas no instante t (o especialista da M1, atualizado todo passo).

Comparações reportadas: cada variante ÷ COMPLETO e ÷ v0.52. Nada é escolhido; o resultado orienta o redesenho ou o adiamento da M1.
