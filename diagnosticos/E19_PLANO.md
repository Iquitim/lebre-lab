# Diagnóstico E19: M1 rascunho 4 nas marés (VB07, XB07; B07 controle), plano antes de rodar

**Data:** 09/10/2026. Só descrição; não muda a decisão do E18b. No E14, a regressão AR2 + bandas de todas as 3 entradas a
cada 8 passos chega a ~1,04 do comparador completo nas marés; com a M1 r4 a v0.53 fica em 1,12 (VB07) e 1,09 (XB07).
Medidas (`e19_m1.py`, M1 r4 + M2 Q2 como no E18b): MSE ÷ v0.52 de L', do especialista recortado e sem recorte; s médio e
por quinto; fração de passos em sombra; reinícios do Prod (troca do conjunto de entradas); fração no recorte.
Hipóteses: o especialista sozinho é bom, mas (a) o Prod demora ou não chega a dar peso; (b) reinícios por reseleção das
entradas (T_MAX) zeram o Prod e a sombra; (c) o recorte custa.
