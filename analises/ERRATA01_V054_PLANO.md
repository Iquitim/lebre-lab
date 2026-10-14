# Errata 01 da v0.54 (M5b rascunho 2): plano e critérios, escritos e commitados antes de rodar

**Data:** 14/10/2026. **Para quê:** conferir no banco a correção do defeito de pico de custo encontrado pela auditoria de
estresse da v0.54 (lebre-research, `experiments/LEBRE-V0.54-AUDIT-01/RELATORIO_AUDITORIA.md`, commit `b342171`). Na M5b
rascunho 1, a atualização da matriz de covariâncias (só relatório) coincidia periodicamente com a regressão da camada
M1, e o pico por passo subia até 50% com 50 entradas. A M5b rascunho 2 (protótipo no commit `f9906c4`) guarda a mesma
amostra por ciclo e aplica a atualização uma linha por vez.

**Comparação, por série das 64 famílias do E20:**

- **v0.54 com errata:** `Lebre054(..., m5a=True, m5b=True, m4=True)` no commit `f9906c4`;
- **v0.54 promovida:** a mesma configuração com o núcleo da M5b rascunho 1 (`screening.py` do commit `cfe72ce`), o que
  reproduz o commit promovido (o restante do código é igual, e a M6 está desligada);
- **v0.53:** `lebre==0.2.0`.

Custo por passo medido a cada passo, antes de qualquer consulta ao relatório. Script: `analises/errata01_v054.py`.

## Critérios (fixados antes)

1. **Identidade com a v0.54 promovida:** previsões idênticas passo a passo, estrutura final idêntica e relatório de
   equivalentes idêntico no fim (todas as unidades de entrada ativas), em todas as séries.
2. **Custo médio:** igual ao da v0.54 promovida (diferença relativa ≤ 10⁻⁹) em todas as séries.
3. **Pico:** em cada família, o maior custo de um passo da v0.54 com errata ≤ 1,10 × o da v0.53 (o sinal de alerta da
   auditoria). Reporta-se também o pico da v0.54 promovida.

**Regra:** a errata 01 é **aceita** se atender a 1, 2 e 3; se não, as falhas são declaradas e nada é ajustado.
