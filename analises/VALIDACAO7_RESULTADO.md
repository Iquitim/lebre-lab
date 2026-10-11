# Validação 7 (v0.54, M5b rascunho 1 e M4 rascunho 1): resultado

Regras e critérios em `VALIDACAO7_PLANO.md`; congelamento em `VALIDACAO7_CONGELADA.md`. Protótipo no commit `cfe72ce`; cada mudança contra a v0.54 com a M5a. Usada uma única vez.

| Família | séries | M5b: idênticas | núcleo sem → com | M4: razão de MSE | IC 95% | remoções |
|---|---|---|---|---|---|---|
| T-A01 | 30 | 30 | 1719 → 1354 | 1.0000 | 1.0000–1.0000 | 0 |
| T-A05 | 20 | 20 | 382 → 373 | 0.9994 | 0.9987–1.0001 | 20 |
| T-A07 | 20 | 20 | 308 → 302 | 1.0038 | 1.0028–1.0048 | 2 |
| T-A02 | 20 | 20 | 396 → 380 | 1.0000 | 1.0000–1.0000 | 0 |
| T-B03 | 4 | 4 | 838 → 795 | 1.0000 | 1.0000–1.0000 | 0 |
| T-B06 | 6 | 6 | 611 → 596 | 0.9999 | 0.9994–1.0004 | 0 |

**M5b rascunho 1**

1. Identidade: atende
2. Custo (nunca maior; menor onde a triagem roda; razão T-A01 d = 50: 0.719, limite 0,80): atende
3. Equivalentes (fora da faixa: 0 discordâncias em 1863 pares; dentro: 0, só reportado): atende

**Decisão pela regra do plano:** a M5b (rascunho 1) é **aceita**.

**M4 rascunho 1**

1. T-A05 (x0 removida até 10.000 passos depois da troca, ≥ 14 de 20): 20 de 20 — atende
2. Sem remoções falsas (T-A01: 0; T-A02: 0): atende
3. Sem piora (limite superior ≤ 1,02 em todas; nenhuma previsão não finita): atende
4. Identidade onde nenhuma unidade foi aceita: atende

**Decisão pela regra do plano:** a M4 (rascunho 1) é **aceita**.

## Ressalva (depois da decisão; não a altera)

Em 2 das 20 séries de T-A07 (relação intermitente em blocos de 5.000 passos), a M4 removeu x0 no passo ~10.100, logo
quando a relação voltava: o teste disparado abriu no início do bloco desligado, juntou os 5.000 passos mínimos de
evidência durante esse bloco e aceitou bem no retorno. A duração mínima coincide com o tamanho do bloco deste gerador. O
efeito ficou dentro do critério (T-A07: 1,0038, limite superior 1,0048), mas a fraqueza é real e fica declarada:
relações que somem por um período igual ou maior que 5.000 passos e depois voltam podem ser removidas e precisar ser
redetectadas.
