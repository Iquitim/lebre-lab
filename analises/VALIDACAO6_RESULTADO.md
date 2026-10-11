# Validação 6 (v0.54, M5a rascunho 2): resultado

Regras e critérios em `VALIDACAO6_PLANO.md`; congelamento em `VALIDACAO6_CONGELADA.md`. Protótipo no commit `f69dec4`; referência `lebre==0.2.0`. Usada uma única vez.

| Família | séries | v0.54 ÷ v0.53 (MSE) | IC 95% | M1 dormiu | custo da M1 v0.53 → v0.54 | razão | custo total v0.53 → v0.54 |
|---|---|---|---|---|---|---|---|
| U-A01 | 30 | 1.0000 | 1.0000–1.0000 | 30 | 819 → 308 | 0.377 | 2678 → 2168 |
| U-A05 | 20 | 1.0000 | 1.0000–1.0000 | 20 | 401 → 92 | 0.229 | 923 → 614 |
| U-B02 | 4 | 1.0000 | 1.0000–1.0000 | 4 | 754 → 260 | 0.345 | 1669 → 1175 |
| U-B03 | 4 | 0.9959 | 0.9843–1.0059 | 4 | 734 → 475 | 0.647 | 1700 → 1441 |
| U-B06 | 6 | 0.9994 | 0.9984–1.0003 | 6 | 772 → 553 | 0.716 | 1544 → 1324 |
| U-B07 | 6 | 0.9948 | 0.9919–0.9974 | 6 | 394 → 321 | 0.815 | 948 → 875 |

1. **Custo** (U-A01 e U-A05, razão ≤ 0,40): atende
2. **Sem piora** (limite superior ≤ 1,01 em todas; nenhuma previsão não finita): atende
3. **Identidade** onde a M1 nunca dormiu: atende

**Decisão pela regra do plano:** a M5a (rascunho 2) é **aceita**.

## Leitura (descritiva)

- Custo da M1 nas famílias reais: corte de 65% na carga (U-B02), 35% no ar de Pequim (U-B03), 28% na eólica (U-B06) e
  18% nas marés (U-B07); nas três últimas a M1 desperta várias vezes ao longo da série. Custo total por passo de 7% a 30%
  menor nas famílias reais.
- Precisão: igual à v0.53 nas sintéticas e na carga; ligeiramente melhor no ar de Pequim (0,996), na eólica (0,999) e nas
  marés (0,995, IC 0,992–0,997).
- **Ressalva:** a meta de custo usada aqui (corte ≥ 60%) foi revista pelo responsável pelo projeto depois de três medições
  no desenvolvimento (a original era 75%); esta validação foi o primeiro teste da M5a com essa meta, em dados novos.
