# Fontes de dados

Cada conjunto é registrado aqui **antes** de ser baixado. Dados brutos não entram no git.

| Conjunto | Cenários | Fonte (URL) | Licença | Permite redistribuir? | Conferido em |
|---|---|---|---|---|---|
| UCI Air Quality (De Vito 2008), horário, mar/2004 a fev/2005, uma cidade italiana | B03 | https://archive.ics.uci.edu/dataset/360/air+quality (doi:10.24432/C59K5F) | CC BY 4.0 | Sim, com atribuição | 2026-10-04 |
| ONS, Curva de Carga Horária, por subsistema | B02 | https://dados.ons.org.br/dataset/curva-carga | CC-BY (atribuição ao ONS e indicação de alterações) | Sim, com atribuição | 2026-10-04 |
| ONS, Fator de Capacidade Eólica e Solar, horário por usina, com coordenadas | B01, B06 | https://dados.ons.org.br/dataset/fator-capacidade-2 | CC-BY (atribuição ao ONS e indicação de alterações) | Sim, com atribuição | 2026-10-04 |
| Open-Meteo, API histórica (reanálise ERA5 / Copernicus) | B01, B02, B06 | https://open-meteo.com/en/terms | CC BY 4.0; o API gratuito é só para uso não comercial (este projeto não é comercial) | Sim, com atribuição (Open-Meteo e Copernicus/ERA5) | 2026-10-04 |
| NOAA CO-OPS (Tides and Currents): nível do mar, maré prevista, vento e pressão | B07 | https://tidesandcurrents.noaa.gov/disclaimers.html | Domínio público (atribuição solicitada) | Sim | 2026-10-04 |
| InfoDengue (casos semanais por município) | B04 | https://info.dengue.mat.br/services/api | **Nenhuma licença explícita** na documentação | Não confirmado: **não usar** | 2026-10-04 |
| OpenDataSUS, SINAN Dengue (notificações individuais) | B04 | https://opendatasus.saude.gov.br (redireciona para dadosabertos.saude.gov.br) | Indicação de Creative Commons com atribuição em fontes secundárias; **não confirmada na página do conjunto** | Não confirmado: B04 adiado até confirmar | 2026-10-04 |
| Métricas de servidor | B05 | nenhuma fonte escolhida | — | — | B05 adiado |
| Banco Central do Brasil, SGS: dólar PTAX diário (1) e Selic acumulada no mês (4390) | C01-C05 | https://dadosabertos.bcb.gov.br (licença conferida nas páginas das séries 1 e 4390) | ODbL (Open Database License) | Sim, com atribuição e mantendo a mesma licença em bases derivadas | 2026-10-04 |
| IBGE: IPCA (433) e INPC (188), lidos pelo SGS do BCB | C05 | https://dados.gov.br/dados/conjuntos-dados/ia-indice-nacional-de-precos-ao-consumidor-amplo-ipca; política do IBGE: reuso permitido citando o IBGE como fonte | Domínio público no portal federal; reuso com citação | Sim, citando o IBGE | 2026-10-04 |
| FGV: IGP-M (189) | (C05, descartado) | — | Licença da FGV não conferida | **Não usar** | 2026-10-04 |
| FRED: DGS10, DGS2, DTB3 (Fed H.15), DEXUSEU, DEXJPUS (Fed H.10), DCOILWTICO (EIA) | C01-C04 | https://fred.stlouisfed.org (status conferido na página de cada série); termos: https://fred.stlouisfed.org/legal/ | Domínio público, citação solicitada | Sim | 2026-10-04 |
| FRED: DEXINUS, DEXSIUS, DEXTHUS, DEXDNUS (Fed H.10), DGS1, DGS5, DGS30 (Fed H.15) | validação 2 (W-C01 a W-C04) | https://fred.stlouisfed.org (etiqueta "Public Domain: Citation Requested" conferida na página de cada série); termos: https://fred.stlouisfed.org/legal/ | Domínio público, citação solicitada | Sim | 2026-10-08 |
| FRED: DEXMAUS, DEXTAUS, DEXSLUS, DEXSFUS (Fed H.10), DGS3, DGS7, DGS20 (Fed H.15) | validação 3 (X-C01 a X-C04) | https://fred.stlouisfed.org (etiqueta "Public Domain: Citation Requested" conferida na página de cada série); termos: https://fred.stlouisfed.org/legal/ | Domínio público, citação solicitada | Sim | 2026-10-08 |
| FRED: DEXUSNZ (Fed H.10) | validação 5 (Z-C01 a Z-C03) | https://fred.stlouisfed.org (etiqueta "Public Domain: Citation Requested" conferida na página da série); termos: https://fred.stlouisfed.org/legal/ | Domínio público, citação solicitada | Sim | 2026-10-09 |
| FRED: VIXCLS e S&P 500 | (C02, descartado) | https://fred.stlouisfed.org/legal/ | Copyright do fornecedor (CBOE, S&P) | Não sem permissão: **não usar** | 2026-10-04 |

## Observações de uso

- **Meteorologia de reanálise não é previsão.** A Open-Meteo histórica fornece o tempo que de fato ocorreu (ERA5).
  Usá-la como entrada mede se a LEBRE encontra a relação física, mas dá um resultado otimista em relação ao uso real,
  em que se teria uma previsão do tempo. Os cenários que a usam dizem isso explicitamente.
- **Geração programada do ONS não é usada como entrada** nos cenários B01 e B06: ela é um plano feito com informação
  que a LEBRE não tem, e tornaria a tarefa trivial.
- Atribuições exigidas em qualquer material derivado: ONS (Dados Abertos); Open-Meteo e Copernicus Climate Change
  Service (ERA5); De Vito, S. (2008), UCI; NOAA National Ocean Service; Banco Central do Brasil (SGS); IBGE;
  Board of Governors of the Federal Reserve System e U.S. Energy Information Administration, via FRED.
- O código só baixa do FRED as séries de domínio público listadas acima (`lab/fontes.py` recusa as outras).
