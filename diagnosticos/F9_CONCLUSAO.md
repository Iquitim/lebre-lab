# Diagnóstico F9: conclusão (06/10/2026, 06:26; dentro do limite de 20 minutos)

Resultado completo em `F9_RESULTADO.json`; pergunta e regra em `F9_PERGUNTA.md` (commit anterior à execução).

**1. As aceitações quase não mudaram as previsões.** Nas 4 entradas aceitas, a razão de MSE entre a LEBRE normal e a
LEBRE sem entradas externas ficou entre 0,995 e 1,009, antes e depois da aceitação. Pela regra declarada, as classes
saem misturadas (1 "existiu e ficou", 1 "existiu e sumiu", 2 "nunca existiu"), mas as diferenças são menores que 1%:
a regra não previa margem de empate, o que é uma falha dela. Leitura honesta: **efeito desprezível**.

**2. A perda contra o passeio aleatório não vem das entradas.** Razão de MSE contra o passeio aleatório, depois do
aquecimento:

| Série | LEBRE normal | LEBRE sem entradas |
|---|---|---|
| dólar/real | 1,045 | 1,045 |
| euro/dólar | 1,030 | 1,031 |
| iene/dólar | 1,050 | 1,050 |
| petróleo WTI | 1,153 | 1,189 |

**Conclusão:** em precisão, F9 é o mesmo problema de F8: a memória e o modelo base se adaptam ao ruído e ficam atrás da
referência trivial (aqui, o passeio aleatório). As entradas espúrias são um problema de **interpretação** (a lista de
aceitas engana), não de precisão.

**Consequência para a v0.53:** M2 (partir da referência trivial e só se afastar com evidência) passa a cobrir F8 e a
parte de precisão de F9; M3 (não estacionariedade) cai de prioridade e fica restrito à interpretação das aceitas.

**A investigar depois (fora do limite de tempo):** margem de empate na regra; por que a aceitação passa no teste com
efeito tão pequeno (o e-process mede melhora acumulada; uma melhora mínima e persistente pode bastar).
