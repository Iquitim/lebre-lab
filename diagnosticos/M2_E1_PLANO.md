# Diagnóstico E1 da M2 (só descrição, nenhuma escolha): plano

**Data:** 08/10/2026. **Por quê:** a reflexão `REFLEXAO_M2.md` (lebre-research) separa duas dificuldades: D1 (a LEBRE
aprende) e D2 (diferenças pequenas). Antes de desenhar um novo candidato, descrever o mecanismo nas séries que derrubaram
os rascunhos 4 e 6. Dados de desenvolvimento e da validação 1 (já gasta para seleção), sem efeito sobre qualquer escolha.

**Séries:** C04 juros de 2 anos; B01 Arinos; VC05 IPCA serviços; C05 IPCA. **Configurações:** rascunho 4
(`adahedge_recortada`) e 6 (`adahedge_compartilhada_rapida`), protótipo no commit atual.

**Descrito por série e configuração:** razão de MSE contra v0.52 e contra a referência na janela de avaliação; peso de L
em quantis da série; η em quantis; diferença acumulada de perda recortada (R − L) em pontos da série; fração da janela de
avaliação com peso de L > 0,5.
