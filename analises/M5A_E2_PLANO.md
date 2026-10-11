# Medição M5A_E2 (desenvolvimento da v0.54): M5a rascunho 1. Plano antes de rodar

**Data:** 10/10/2026. **Especificação:** lebre-research, `experiments/LEBRE-V0.54-DESIGN-NOTE-01/ALGORITHM_SPEC_DRAFT_M5a_r1.md`
(commit `1a7ff44`). **Código:** protótipo `experiments/LEBRE-V0.54-PROTO-01` (`Lebre054`, rascunho 1) numa cópia fixa
(git worktree) do commit `1a7ff44`; referência: `lebre==0.2.0`. Mesmo método e mesmos geradores do M5A_E1
(`analises/m5a_e1.py`, sem alteração); o script `analises/m5a_e2.py` só troca as sementes, a pasta de saída e o critério
de custo. Antecedente: M5A_E1 (rascunho 0, revisão a), não aceito.

## Critérios (os do rascunho 1)

1. **Custo:** A01 (30 séries) e A05 (20): custo médio da M1 na v0.54 ≤ 0,25 × o da v0.53, em cada cenário. C03 só reportado.
2. **Sem piora:** 64 famílias do E20: limite superior do IC 95% (bootstrap de blocos pareado, semente 20261061) ≤ 1,01;
   nenhuma previsão não finita.
3. **3a:** sementes 20261111 a 20261130; MSE depois da troca, v0.54 ÷ v0.53 (geo, 20) ≤ 1,02.
4. **3b:** sementes 20261131 a 20261150; despertar condicional em ≥ 90% das séries na condição (inconclusivo com menos de
   5; ativa em t = 24.000 conta como despertada); MSE do último trecho (geo, 20) ≤ 1,02.
5. **Identidade:** onde a M1 nunca dormiu, previsões idênticas às da v0.53.

**Regra:** a M5a (rascunho 1) fica se atender a 1, 2, 3a, 3b e 5. Falhas declaradas, nada ajustado. Saída:
`analises/m5a_e2/` e `analises/M5A_E2_RESULTADO.md`.
