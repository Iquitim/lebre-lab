# LEBRE Lab

Testes exploratórios da versão congelada da [LEBRE](https://github.com/Iquitim/lebre) (`lebre==0.1.0`, algoritmo
v0.52-r1) em situações novas: estresse com dados sintéticos, novos domínios, mercado financeiro e ensembles construídos em volta dela.

- O plano, as regras e o catálogo de testes estão em [`PLANO.md`](PLANO.md).
- Cada execução fica registrada em [`runs/REGISTRO.csv`](runs/), inclusive as que falharam.
- O que aprendemos vai para [`MAPA.md`](MAPA.md) (quando usar) e [`FALHAS.md`](FALHAS.md) (o que melhorar).

Os resultados aqui são **exploratórios**: não substituem a avaliação pré-registrada da pesquisa
([lebre-research](https://github.com/Iquitim/lebre-research)).

## Ambiente

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q                       # testa o código comum
.venv\Scripts\python -m lab.run scenarios/A/<cenario>.py --ensaio   # confere um cenário sem registrar
.venv\Scripts\python -m lab.run scenarios/A/<cenario>.py            # roda e registra (exige tudo commitado)
```
