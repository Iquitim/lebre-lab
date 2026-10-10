# Medição M5A_E1 (desenvolvimento da v0.54): M5a rascunho 0, revisão a. Plano antes de rodar

**Data:** 10/10/2026. **Especificação:** lebre-research, `experiments/LEBRE-V0.54-DESIGN-NOTE-01/ALGORITHM_SPEC_DRAFT_M5a.md`
(rascunho 0, revisão a, commit `86bf359`). **Código:** protótipo `experiments/LEBRE-V0.54-PROTO-01` (`Lebre054`), numa
cópia fixa (git worktree) do commit registrado no resultado; referência: a v0.53 publicada (`lebre==0.2.0`, `Lebre`), com
a mesma referência trivial (zero se a série pede, senão sazonal se há ciclo, senão persistência). O script recusa rodar
com o protótipo alterado e não commitado, ou com outra versão da biblioteca. Dados: só desenvolvimento do Lab (as travas
das reservas da v0.53 e da v0.54 continuam valendo). Não é evidência independente.

## Critérios (os da especificação; nada é ajustado depois)

1. **Custo:** em A01 (30 séries), A05 (20) e C03 (4), custo médio da M1 por passo na v0.54 ≤ 0,25 × o da v0.53, em cada
   cenário. Reporta-se também o custo total por passo.
2. **Sem piora:** nas 64 famílias do E20 (mesma lista e mesmas séries, `analises/m2_e20._series`), razão de MSE
   v0.54 ÷ v0.53 por família, média geométrica das séries, com IC 95% por bootstrap de blocos pareado (mesmo método e
   tamanhos de bloco do E20; semente 20261060): limite superior ≤ 1,01 em todas; nenhuma previsão não finita no trecho
   avaliado (depois de 20% da série).
3. **3a — sem piora depois da troca de regime:** 20 séries (sementes 20261070 a 20261089), T = 30.000, 4 entradas AR(1)
   com coeficiente 0,6; até t = 15.000, y = 0,8 x0(t − 3) + 0,6 ruído; depois, y = 1,2 y(t − 1) − 0,35 y(t − 2) +
   0,6 média(x0, t − 2…t − 3) + 0,4 média(x1, t − 4…t − 7) + 0,3 ruído. MSE da v0.54 no trecho t ≥ 15.000 dividido pelo da
   v0.53, média geométrica das 20 séries: ≤ 1,02.
4. **3b — despertar condicional:** 20 séries (sementes 20261090 a 20261109), T = 36.000, mesmas entradas; regime A
   (a dinâmica conjunta acima) em t < 12.000 e em t ≥ 24.000; regime B em 12.000 ≤ t < 24.000: y(t) = y(t − 1) + 0,5
   ruído (passeio aleatório, entradas irrelevantes). Condição: a M1 da v0.53 volta a pesar (ω > 0,5 em algum passo de
   t ≥ 24.000) **e** a M1 da v0.54 dormiu antes de t = 24.000. Critério: nas séries que satisfazem a condição, a M1 da
   v0.54 desperta em t ≥ 24.000 em pelo menos 90% delas (se em t = 24.000 ela já estiver ativa, conta como
   despertada); e o MSE do trecho t ≥ 24.000, v0.54 ÷ v0.53 (média geométrica
   das 20), ≤ 1,02. Se menos de 5 séries satisfizerem a condição, a parte do despertar é declarada **inconclusiva** (não
   aprovada).
5. **Identidade:** em toda série do item 2 em que a M1 da v0.54 nunca dormiu, previsões idênticas às da v0.53 (igualdade
   exata de ponto flutuante).

**Regra:** a M5a (rascunho 0, revisão a) fica se atender a 1, 2, 3a, 3b e 5. Falhas declaradas; qualquer mudança de
constantes depois deste ponto é um novo rascunho. Saída: `analises/m5a_e1/` (JSON por família e por cenário) e
`analises/M5A_E1_RESULTADO.md`.
