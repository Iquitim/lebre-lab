# Experimento E2 da M2 (desenvolvimento): plano, escrito e commitado antes de rodar

**Data:** 08/10/2026. **Contexto:** `REFLEXAO_M2.md` e o diagnóstico E1 (`diagnosticos/M2_E1_RESULTADO.md`). O rascunho 2
(AdaHedge sobre o erro quadrático, a régua dos critérios) falhou só nas séries curtas de B02, por causa dos primeiros 24
passos, em que a referência sazonal ainda não existe (o código usava persistência no lugar). A variante D compara só os
passos em que a referência declarada está definida.

**Natureza:** desenvolvimento. Dados: as 23 famílias do banco de desenvolvimento e as 10 da validação 1 (gasta para
seleção, usada aqui como desenvolvimento). **Nenhum resultado daqui é evidência de seleção para a v0.53.**

**Configurações:** H (rascunho 2, "adahedge", para comparação) e D ("adahedge_ref_definida"). Protótipo no commit
`a0e20e1` do lebre-research. Mesmos critérios, bootstrap (semente 20261015) e grupos de `M2_DEV_R6_PLANO.md`.

**Regra (fixada antes):** se D atender a todos os critérios nas 33 famílias, D passa a candidata da M2 e vai à
**validação 2** (nova, a montar e congelar antes de qualquer medição dela) e depois à reserva final. Se não atender, as
falhas orientam o próximo passo (sem seleção). Contagem de tentativas: D é a sétima configuração.
