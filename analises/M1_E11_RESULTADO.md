# Experimento E11 (M1 rascunho 1 + M2, desenvolvimento): resultado (parcial, interrompido)

Plano `M1_E11_PLANO.md`. **A M1 rascunho 1 não fica.** Falha o critério 3 em W-CURTAS (critério 2 da M2: 1,020, limite
superior 1,046). A execução de W-B02/B02 abortou (saída não finita). Interrompida com a regra decidida; famílias restantes
e o script dos critérios próprios (F6) não concluídos.

## Diagnóstico (observação; nada foi alterado)

Em W-B02 (5 entradas, k = 28 variáveis), o especialista entra no Prod depois de exatamente k atualizações da RLS: o sistema
está determinado, mas mal condicionado (coeficientes até 8.600; previsão de 153 mil MW para uma carga de 28 mil). O Prod
avalia o especialista pela perda recortada (no máximo 1 por passo), mas a saída é a mistura em erro quadrático: um
especialista "selvagem" custa pouco ao Prod e muito à saída, sem limite. Na M2 isso não ocorria porque as saídas combinadas
(D e M) ficam sempre entre a referência e a v0.52. Os valores enormes produziram depois um NaN na M2. A falha em W-CURTAS
é compatível com o mesmo mecanismo (especialista recém-liberado no fim das séries curtas).
