# Diagnóstico E19: M1 rascunho 4 nas marés (resultado)

Plano `E19_PLANO.md`. Só descrição. Dados: `e19_m1.json`.

- **O especialista é bom e o Prod quase não o usa.** O especialista sozinho (recortado) é melhor que a v0.52 em 15 das 18
  séries (0,76 a 0,97; St. Petersburg 0,757), mas o peso s fica em ~0 o período todo em 8 séries (St. Petersburg, La Jolla,
  Woods Hole, Los Angeles, The Battery, Atlantic City, Charleston, Key West) e só sobe no fim em outras (Baltimore: 0 → 0,42;
  Sewells Point: 0 → 0,996 só no último quinto).
- **(b) e (c) descartadas:** nenhum reinício do Prod (sem troca de entradas), nenhum passo em sombra no período de avaliação;
  o recorte atua em < 1,5% dos passos (exceto St. Petersburg, onde custa: 0,632 sem, 0,757 com).
- **Leitura (hipótese):** normalizar as perdas pelo maior erro **com esquecimento** é o mesmo que dar a cada passo um peso
  inverso à escala recente do erro; passos de erro grande (marés meteorológicas, tempestades), onde o especialista ganha,
  pesam pouco, e os passos calmos pesam muito. O Prod passa a otimizar outra coisa que não o MSE. Com o máximo sem
  esquecimento (Q, rascunho 3), o Prod congela. As duas formas de pôr o erro quadrático em [0, 1] para o Prod falharam por
  razões opostas: o problema é a exigência de perdas limitadas, não o ajuste da normalização.
