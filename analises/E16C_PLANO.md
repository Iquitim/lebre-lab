# Releitura E16c: candidatas Q e Q2 com a régua do adendo 3, plano antes de rodar

**Data:** 09/10/2026. Depois do E18b, o responsável pelo projeto decidiu o adendo 3 da régua (`M2_CANDIDATA_D.md`,
lebre-research `b1f9389`): o limite do choque passa a ser máx(5%, 5 × 2 ln(n)/n), n = passos avaliados. Como a escolha
entre Q e Q2 (`M2_CANDIDATA_Q2.md`, seção 2) foi feita com a régua anterior, as duas são **relidas com a régua nova**, no
mesmo desenvolvimento ampliado (64 famílias), com o script `m2_e16c.py` (sementes novas 20261047 e 20261048; protótipo
`fc71880`; NaN contado como falha). **Regra de escolha (a mesma, declarada antes):** se as duas atenderem, fica a Q2; se só
uma, fica ela; se nenhuma, falhas declaradas e a M2 volta ao desenho. É desenvolvimento, não evidência; a evidência será a
validação 5.

**Adendo (09/10/2026, durante a execução):** 8 dos 14 processos foram parados pela guarda de protótipo não commitado
(edição da M1 rascunho 5 durante a execução). As famílias que faltavam rodam de novo com o commit `bca5dac`, que só
acrescenta o rascunho 5 da M1 (Q e Q2 idênticas bit a bit, conferido). Daqui em diante, as medições rodam numa cópia fixa do
protótipo (git worktree num commit determinado).
