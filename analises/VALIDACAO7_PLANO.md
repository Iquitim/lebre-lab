# Validação 7 (v0.54, M5b rascunho 1 e M4 rascunho 1): regras de escolha e critérios, escritos e commitados antes de baixar qualquer dado

**Data:** 11/10/2026. **Para quê:** decidir, em séries que nenhuma medição viu, as duas mudanças da v0.54 revistas depois
de uma medição no banco:

- **M5b rascunho 1** (`ALGORITHM_SPEC_DRAFT_M5b.md` no lebre-research): matriz de covariâncias das entradas atualizada a
  cada 31 passos (só relatório);
- **M4 rascunho 1** (`ALGORITHM_SPEC_DRAFT_M4.md`): teste de remoção disparado pela queda da contribuição, acrescentado
  ao calendário original, com duração mínima de 5.000 passos para aceitar.

Cada uma é medida separadamente contra a v0.54 com a M5a aceita (ablação). Usada **uma única vez**. Regras gerais como nas
validações 1 a 6: escolha só por metadados, listas ou sementes declaradas aqui; nada das reservas das avaliações finais da
v0.53 e da v0.54, do desenvolvimento nem das validações 1 a 6 como alvo; congelamento com SHA-256 antes da medição;
substituição só pela regra da família.

| Família | Análoga a | Regra de escolha |
|---|---|---|
| T-A01 | A01 (custo) | Gerador de A01; d = 10, 20 e 50, 10 séries cada; sementes 2026101200 a 2026101229 (10 por grupo, na ordem). |
| T-A05 | A05 (troca de regime) | Gerador de A05; 20 séries; sementes 2026101230 a 2026101249. |
| T-A07 | A07 (relação intermitente) | Gerador de A07; 20 séries; sementes 2026101250 a 2026101269. |
| T-A02 | A02 (nulo) | Gerador de A02; 20 séries; sementes 2026101270 a 2026101289. |
| T-B03 | B03 | UCI *Beijing Multi-Site Air Quality* (CC BY 4.0), mar/2013 a fev/2017, **quarta estação em ordem alfabética** (as três primeiras foram usadas nas validações 4 a 6). Alvos e entradas como em U-B03; ciclos 24 e 168. |
| T-B06 | B06 (eólica) | Usinas eólicas a partir da 37ª por capacidade (`lab/usinas.escolher`, mesmo filtro), 2024-2025, **pulando as da reserva da v0.54 e as 6 da validação 6**, até 6 (mínimo 3, senão a família sai e isso é declarado); ciclo 24. |

Fora, e declarado: carga (2000 a 2025 já usados; 2026 é da reserva da v0.53), solar (esgotada; 2026 é da reserva da
v0.54), maré (as estações da lista usada até agora foram consumidas), câmbio e juros (esgotados ou reservados). Sementes
2026101200 a 2026101299 conferidas como não usadas no código e nos documentos dos três repositórios.

## Critérios (os das medições no banco, fixados antes)

**M5b rascunho 1** (`m5b=False` contra `m5b=True`), em todas as famílias:

1. **Identidade:** previsões idênticas passo a passo e estrutura final idêntica em todas as séries.
2. **Custo:** custo do núcleo nunca maior, menor em toda série em que a triagem roda; razão ≤ 0,80 na média do grupo
   d = 50 de T-A01.
3. **Relatório de equivalentes:** fora da faixa 0,90 ≤ |r| ≤ 0,98, pertinência idêntica no fim de cada série.

**M4 rascunho 1** (`m4=False` contra `m4=True`):

1. **T-A05:** x0 removida entre a troca (passo 15.000) e 10.000 passos depois, em pelo menos 14 de 20 séries.
2. **Sem remoções falsas:** T-A01, nenhuma remoção de x0 ou x1; T-A02, nenhuma série com entrada externa na estrutura
   final.
3. **Sem piora:** em cada família, razão de MSE (média geométrica), IC 95% por bootstrap de blocos pareado (blocos de
   168 nas famílias B, 20 nas A; semente 2026101290): limite superior ≤ 1,02; nenhuma previsão não finita no trecho
   avaliado (depois de 20% da série).
4. **Identidade:** onde nenhuma unidade foi aceita sem a M4, previsões idênticas.

**Código:** protótipo `experiments/LEBRE-V0.54-PROTO-01` no commit `cfe72ce` (contém a M5b rascunho 1 e a M4 rascunho 1;
git worktree fixo), referência `lebre==0.2.0`.
**Regra:** cada mudança é **aceita** se atender a todos os seus critérios; se não, as falhas são declaradas e nada é
ajustado.
