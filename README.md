# LEBRE Lab

Banco de testes e de desenvolvimento da [LEBRE](https://github.com/Iquitim/lebre-research). Começou com testes
exploratórios da versão congelada `lebre==0.1.0` (algoritmo v0.52-r1) e virou o **banco de desenvolvimento da v0.53**:
todas as medições de desenho, as validações 1 a 5 e os diagnósticos que levaram à v0.53 estão aqui.

A v0.53 foi promovida em 09/10/2026 por uma avaliação final pré-registrada, feita no
[lebre-research](https://github.com/Iquitim/lebre-research) com dados reservados antes de qualquer código da v0.53
(`docs/architecture/LEBRE_v0.53_FREEZE_RECORD.md` e `experiments/LEBRE-V0.53-FINAL-01/` lá). Os resultados deste
repositório são **desenvolvimento e validação**: só a avaliação final é evidência vinculante.

## Onde está cada coisa

| Pasta ou arquivo | Conteúdo |
|---|---|
| [`PLANO.md`](PLANO.md), [`MAPA.md`](MAPA.md), [`FALHAS.md`](FALHAS.md) | Plano e regras do Lab; quando usar a LEBRE; o que melhorar (a origem dos itens F1 a F9 da v0.53). |
| `scenarios/A` a `D` | Cenários do desenvolvimento (sintéticos, dados reais, finanças, ensembles). |
| `scenarios/V`, `W`, `X`, `Y`, `Z` | Validações 1 a 5 (cada uma usada uma única vez). |
| `analises/` | Planos e resultados das medições da M1 e da M2 (`*_PLANO.md` commitado antes de rodar, `*_RESULTADO.md`), regras e registros de congelamento das validações (`VALIDACAO*_PLANO.md`, `VALIDACAO*_CONGELADA.md`), erratas. |
| `diagnosticos/` | Diagnósticos só descritivos (E1 a E22), também com plano antes. |
| `runs/` | Registro de cada execução dos cenários (`REGISTRO.csv`), inclusive as que falharam. |
| `lab/` | Código comum: fontes de dados, comparadores, métricas, travas da reserva da v0.53 (`reserva.py`). |
| `dados/` | Só a lista de fontes e licenças (`FONTES.md`) e os manifestos SHA-256 dos dados usados; **os dados brutos não estão no git** e são baixados das fontes originais pelos próprios cenários. |

## Regras que valem para tudo aqui

- Plano e critérios commitados **antes** de cada medição; nada ajustado depois; falhas declaradas.
- Cada conjunto de validação escolhido só por metadados, congelado com SHA-256 e usado **uma única vez**.
- A reserva da avaliação final da v0.53 nunca é carregada aqui: `lab/reserva.py` recusa essas séries.
- Erratas ficam registradas junto dos resultados (por exemplo, `analises/ERRATA_SEASON_VALIDACOES_4_5.md`).

## Ambiente

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q                       # testa o código comum
.venv\Scripts\python -m lab.run scenarios/A/<cenario>.py --ensaio   # confere um cenário sem registrar
.venv\Scripts\python -m lab.run scenarios/A/<cenario>.py            # roda e registra (exige tudo commitado)
```

As medições da v0.53 (`analises/m1_*.py`, `analises/m2_*.py`, `diagnosticos/*.py`) importam o protótipo do
lebre-research: defina `LEBRE053_PROTO` com a pasta `experiments/LEBRE-V0.53-PROTO-01` de uma cópia dele (de preferência
um `git worktree` no commit registrado em cada resultado; os scripts recusam rodar com o protótipo alterado e não
commitado) e rode como módulo a partir da raiz do Lab, por exemplo `python -m analises.m1_val5 --resumo`.

## Licença

Código e documentos: Apache-2.0 (`LICENSE`). Os dados de terceiros não estão incluídos e mantêm as próprias licenças
(`dados/FONTES.md`).
