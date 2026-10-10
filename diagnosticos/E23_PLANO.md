# Diagnóstico E23: linha de base da v0.53 para as prioridades da v0.54. Plano antes de rodar

**Data:** 10/10/2026. **Natureza:** só descritivo; não aprova nem reprova nada. Fixa os números de partida da nota de
desenho da v0.54 (prioridades decididas pelo responsável pelo projeto em 10/10/2026: 1 = custo proporcional ao uso, M5;
2 = remoções que acontecem e interpretação em séries não estacionárias, M4 + M3; 3 = ciclo como hipótese, M6).

**Modelos:** a v0.53 como publicada (`lebre==0.2.0`, instalada do PyPI; `Lebre` com os padrões: referência sazonal se há
ciclo declarado, senão persistência) e, lado a lado, o núcleo sozinho (`Lebre(..., core_only=True)`, idêntico à
`lebre==0.1.0`). O script recusa rodar com outra versão da biblioteca. Dados: só os cenários de desenvolvimento do Lab
(nenhuma série da reserva da v0.53; `lab/reserva.py` continua valendo). Nada é ajustado.

## Perguntas e medidas

1. **Custo (prioridade 1).**
   - A01 (d = 10, 20, 50; 10 séries cada) e A12 (d = 50, T = 200 mil): custo médio por passo da v0.53 e do núcleo, e a
     parte da M1 e da M2 (contadores internos da biblioteca); recall e entradas falsas (iguais nos dois por construção).
   - Avaliação final da v0.53 (arquivo `final_resultado.json` do lebre-research, já publicado; nenhuma execução nova):
     acréscimo de custo nas séries em que o peso final da M1 é zero.
2. **Remoções (prioridade 2, M4).** A05 (20 séries, troca de regime em t = 15 mil): em quantas a entrada antiga x0 é
   removida; em quantas ela ainda está na estrutura no fim; MSE relativo ao linear online; peso final da M1.
3. **Interpretação em séries não estacionárias (prioridade 2, M3).** C03 (4 séries de níveis): em quantas alguma
   entrada externa é aceita e quantas ficam na estrutura final; MSE relativo ao passeio aleatório, v0.53 e núcleo.
4. **Controle.** A02 (40 séries nulas): séries com entrada falsa aceita (esperado: igual ao núcleo).
5. **Ciclo (prioridade 3, M6).** Séries de D02 (4 de carga, ciclo certo 24 + 168; 6 solares, ciclo 24): MSE da v0.53
   sem declarar ciclo dividido pelo da v0.53 com o ciclo certo; o mesmo para o núcleo (a v0.53 sem ciclo usa a
   persistência como referência).

**Saída:** `diagnosticos/e23_base_v054.json` e `E23_RESULTADO.md` (tabelas por pergunta, com média geométrica das razões
de MSE e o número de séries). Ambiente: `requirements.txt` do Lab com `lebre==0.2.0` no lugar de `lebre==0.1.0`, num
ambiente separado (o ambiente do Lab continua com a 0.1.0).
