# Falhas encontradas

Comportamentos da versão congelada (`lebre==0.1.0`, v0.52-r1) que a próxima versão precisa resolver. Cada item cita a
execução do registro que o mostrou. Nada aqui é corrigido neste projeto.

| # | Falha | Cenário e execução | Gravidade | Observação |
|---|---|---|---|---|
| F1 | Custo por passo cresce em proporção ao número de entradas: ~3.160 operações com 50 entradas, acima do limite de 3.000 declarado | A12, `20261004-181040_A12`; A01, `20261004-175141_A01` | Média | O modelo base e as somas de bandas usam todas as entradas a cada passo, inclusive as que nunca foram aceitas. Uma triagem que desligue candidatas sem sinal reduziria o custo. |
| F2 | Remoções nunca acontecem: depois de uma troca de regime, a entrada antiga fica no modelo | A05, `20261004-180630_A05` | Média | Já observado na pesquisa (margem de remoção lenta). Erro 8% maior que o linear online nesse cenário. Com o limite de 4 unidades ativas, entradas velhas podem acabar bloqueando novas. |
| F3 | Atrasos acima de 31 passos não são vistos | A04, `20261004-175513_A04` | Baixa (limite de desenho) | Bandas até 31. Para dados horários, isso é pouco mais de um dia; para dados de 3 horas, ~4 dias. Uma banda extra ou atraso configurável cobriria mais domínios. |
| F4 | Relações simétricas (como x²) são invisíveis | A10, `20261004-180046_A10` | Baixa (limite de desenho) | Consequência de ser linear. Transformações simples das entradas (\|x\|, x²) como candidatas resolveriam parte. |
| F5 | Com entradas correlacionadas em 0,8, a substituta entra junto com a verdadeira (redundância) | A03, `20261004-175402_A03` | Baixa | Ocupa uma das 4 unidades ativas sem ganho. Com 0,95 a troca pela substituta já era uma limitação declarada. |
