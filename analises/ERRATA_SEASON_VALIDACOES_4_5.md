# Errata (09/10/2026): ciclo errado nas famílias solar, eólica e carga das validações 4 e 5

**O erro:** nos módulos `scenarios/Y/YB01_solar.py`, `YB02_carga.py`, `YB06_eolica.py` (commit `80e800e`, validação 4) e
nas cópias `scenarios/Z/ZB01_solar.py`, `ZB02_carga.py`, `ZB06_eolica.py` (commit `659c4c4`, validação 5), as séries foram
montadas com `season=30` em vez de `season=24` (o ciclo diário usado em B01, B02, B06 do desenvolvimento e nas validações
1 a 3). Causa provável: substituição de texto ao montar os módulos da validação 4 (as posições das usinas mudaram de 19-24
para 25-30, e o "24" do ciclo foi trocado junto); a validação 5 copiou os módulos da 4. Achado ao preparar o pré-registro
final, comparando com `scenarios/B/`.

**Alcance:** validação 4: Y-B01 (6), Y-B02 (4), Y-B06 (6) e 16 das 45 séries de Y-CURTAS; validação 5: Z-B01 (5), Z-B02 (4),
Z-B06 (6) e 14 das 42 de Z-CURTAS. Também as releituras do desenvolvimento ampliado (E16 a E20) que incluíram essas
famílias Y. Não afeta Y/Z-B03, Y/Z-B07, Y/Z-C01 a C05, nem o desenvolvimento original e as validações 1 a 3.

**Efeito:** v0.52 e v0.53 rodaram sobre as mesmas séries, então as comparações entre elas continuam válidas **para a
tarefa como montada**; mas essa tarefa não é a análoga declarada no plano (memória sazonal e referência sazonal com período
30 h, não 24 h; a referência fica mais fraca, o que facilita o critério 1 da régua). Os resultados nessas famílias valem
como evidência sobre outra tarefa, não sobre a família análoga.

**O que muda nas conclusões:** a confirmação da validação 5 continua para F6 (Z-B03, Z-B07) e para Z-C01 a Z-C05. Para
solar, eólica e carga com o ciclo certo, a evidência sobre M1 r5 + M2 Q2 fica sendo o desenvolvimento (E20, com B01, B02,
B06 e as famílias V, W, X dessas fontes, todas com season 24) e a **avaliação final na reserva** (8 usinas solares, 8
eólicas e a carga de 2026, montadas com season 24 e com conferência explícita no código). Nada é rodado de novo nas
validações 4 e 5 (os dados já foram usados).
