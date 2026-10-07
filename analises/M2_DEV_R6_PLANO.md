# Medição da M2, rascunho 6 (última tentativa): plano, escrito e commitado antes de rodar

**Data:** 08/10/2026. **O quê:** protótipo da v0.53 no commit `6a007d2` do lebre-research (o script registra o commit e
o hash de `model053.py`), especificação `ALGORITHM_SPEC_DRAFT_M2_r6.md`: Fixed Share com taxas variáveis (Cesa-Bianchi
et al., 2012, eq. 13), troca α_t = 2/(t+1)² (Adamskiy et al., 2016, seção 4.1.3, ε = 1), η_t pela regra do AdaHedge,
sobre a perda recortada; auditoria como no rascunho 2. **Onde:** as 23 famílias do desenvolvimento **e** as 10 da base de
validação (`VALIDACAO_PLANO.md`, congelada em `VALIDACAO_CONGELADA.md`, commit `38fe907`), usada aqui pela primeira e
única vez.

## 1. Configuração

Uma só, **R6**, sem parâmetros livres.

## 2. Critérios

- **Desenvolvimento:** os de `M2_DEV_R4_PLANO.md` (1 nas negativas C01, C03, C04; 2 nas 19 positivas, **C05 incluída**;
  4; 5 com 75 FP por passo; 6; 7 em CURTAS).
- **Validação:** os de `VALIDACAO_PLANO.md` (1 em VC01, VC03, VC04; 2 em VB01, VB02, VB06, VB07, VC02, **VC05**; 4 em
  VC01, VC04; 5; 6; 7 em VCURTAS).
- Bootstrap de blocos pareado, B = 2000, semente 20261014; blocos 168 (horárias), 20 (dias úteis e sintéticas), 12
  (mensais); nas famílias curtas, 24, 20, 12.

## 3. Regra (fixada antes)

R6 vai à avaliação final na reserva **só se atender a todos os critérios nas duas bases**. Se falhar em qualquer um: a M2
não é resolvida na v0.53, nada é ajustado e não há rascunho 7 neste banco; pela condição do responsável pelo projeto, a
v0.53 não é promovida com a M2. **Todas as 33 famílias são medidas até o fim**, mesmo que a regra se decida antes, porque
é a última medição e o mapa completo das falhas é o registro que fica.

## 4. Ordem de execução

As famílias que mais pesaram nas tentativas anteriores primeiro (C05, CURTAS, B01, C03, C04) e, em paralelo, a validação
inteira; depois o restante.

## 5. Conferências

v0.52 contra o registro do Lab (desenvolvimento); em C05 e B06, a configuração H do rascunho 2 tem de reproduzir
`m2dev_r2/`.
