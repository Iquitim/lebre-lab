# Experimento E20 (desenvolvimento ampliado): M1 rascunho 5, plano escrito e commitado antes de rodar

**Data:** 09/10/2026. **O quê:** a M1 rascunho 5 (`ALGORITHM_SPEC_DRAFT_M1_r5.md`, lebre-research; `precisao="r5"`) com a
**M2 escolhida pela regra da releitura E16c** (`E16C_PLANO.md`: se Q e Q2 atenderem, Q2; se só uma, ela), declarada antes
de conhecer o resultado do E16c. Se nenhuma M2 atender no E16c, o E20 roda com a Q (a que atendeu no E16b) só como
diagnóstico da M1, e isso é declarado no resultado. **Código:** cópia fixa do protótipo (git worktree) no commit `bca5dac`.
**Onde:** o desenvolvimento ampliado (64 famílias). Não é evidência; a confirmação será a validação 5.

**Régua:** por decidibilidade com o adendo 3 (`M2_CANDIDATA_D.md`); sementes 20261049 (medição) e 20261050
(classificação); NaN = falha.

**Critérios:**
1. **F6** (`m2_e20_alvo.py`): em B03, B07, VB07 e XB07, custo da v0.53 <= 2,5 × v0.52 e erro <= 1,05 × o menor erro entre
   as variantes do E14 com custo <= o da v0.53.
2. **Critérios da M2 com M1 + M2** (`m2_e20.py`): 1, 2, 4, 6 e 7 em todas as famílias; custo reportado.

**Regra:** a M1 r5 fica se atender a 1 e 2; então M1 r5 e a M2 escolhida vão juntas para a validação 5. Falhas
declaradas, nada ajustado. Contagem: o rascunho 5 é o 6º desenho da M1.
