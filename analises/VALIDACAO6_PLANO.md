# Validação 6 (v0.54, M5a rascunho 2): regras de escolha e critérios, escritos e commitados antes de baixar qualquer dado

**Data:** 11/10/2026. **Para quê:** decidir a M5a (rascunho 2, `ALGORITHM_SPEC_DRAFT_M5a_r2.md` no lebre-research,
commit `b369a1b`), candidata depois de três medições no desenvolvimento (M5A_E1 a M5A_E3) e da revisão da meta de custo
pelo responsável pelo projeto, em séries que **nenhuma medição viu**. Usada **uma única vez**. Regras gerais como nas
validações 1 a 5: escolha só por metadados, períodos ou listas declaradas aqui; nada das reservas das avaliações finais da
v0.53 e da v0.54, do desenvolvimento nem das validações 1 a 5 como alvo (entidades novas, ou períodos que nenhuma medição
usou para aquela entidade); entradas como nas famílias análogas; congelamento com SHA-256 antes da medição; substituição só
pela reserva da família, na ordem. **Ciclo:** o certo de cada domínio (24 horas; 24 + 168 na carga e no ar de Pequim),
corrigindo a errata das validações 4 e 5.

| Família | Análoga a | Regra de escolha |
|---|---|---|
| U-A01 | A01 (custo) | Mesmo gerador de A01; d = 10, 20 e 50, 10 séries cada; sementes 20261200 a 20261229 (10 por grupo, na ordem). |
| U-A05 | A05 (custo, troca de regime) | Mesmo gerador de A05; 20 séries; sementes 20261230 a 20261249. |
| U-B03 | B03 (F6) | UCI *Beijing Multi-Site Air Quality* (CC BY 4.0), mar/2013 a fev/2017, **terceira estação em ordem alfabética** (a primeira e a segunda foram usadas nas validações 4 e 5). Alvos PM2.5, NO2, CO, O3; entradas como em Z-B03. |
| U-B06 | B06 (eólica) | Usinas eólicas a partir da 37ª por capacidade (`lab/usinas.escolher`, mesmo filtro), 2024-2025, **pulando as da reserva da v0.54**, até 6 (mínimo 3, senão a família sai e isso é declarado). |
| U-B02 | B02 (carga) | Os 4 subsistemas, **2000-2001** (anos que nenhuma medição usou; de 2002 a 2025 todos foram usados e 2026 é da reserva da v0.53); mesma construção, com a meteorologia dos mesmos pontos. |
| U-B07 | B07 (maré) | NOAA CO-OPS 2021-2024, mesma construção: 9419750 Crescent City, 8770570 Sabine Pass (reservas nunca usadas como alvo), 8723214 Virginia Key, 9410170 San Diego, 9455920 Anchorage, 1612340 Honolulu. Reserva, na ordem: 8726724 Clearwater Beach, 9751639 Charlotte Amalie. |

Fora desta validação, e declarado: solar (as usinas elegíveis de 2024-2025 estão esgotadas e a solar de 2026 é da reserva
da v0.54), câmbio e juros (esgotados ou reservados) e séries curtas (a M5a só age depois de ~2.100 passos).

## Critérios (fixados antes; os do rascunho 2 com a meta de custo revista)

1. **Custo:** em U-A01 e U-A05, custo médio da M1 por passo na v0.54 ≤ 0,40 × o da v0.53 (corte ≥ 60%), em cada uma.
2. **Sem piora:** em cada família U, razão de MSE v0.54 ÷ v0.53 (média geométrica das séries), com IC 95% por bootstrap
   de blocos pareado (blocos de 168 nas famílias B, 20 nas A; semente 20261063): limite superior ≤ 1,01; nenhuma previsão
   não finita no trecho avaliado (depois de 20% da série).
3. **Identidade:** onde a M1 da v0.54 nunca dormiu, previsões idênticas às da v0.53.

Reporta-se também o custo da M1 e o total nas famílias reais.

**Código:** protótipo `experiments/LEBRE-V0.54-PROTO-01` no commit `f69dec4` (git worktree), referência `lebre==0.2.0`.
**Regra:** a M5a (rascunho 2) é **aceita** se atender a 1, 2 e 3; se não, falhas declaradas, nada ajustado.
