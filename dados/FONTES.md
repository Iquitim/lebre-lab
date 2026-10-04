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

## Observações de uso

- **Meteorologia de reanálise não é previsão.** A Open-Meteo histórica fornece o tempo que de fato ocorreu (ERA5).
  Usá-la como entrada mede se a LEBRE encontra a relação física, mas dá um resultado otimista em relação ao uso real,
  em que se teria uma previsão do tempo. Os cenários que a usam dizem isso explicitamente.
- **Geração programada do ONS não é usada como entrada** nos cenários B01 e B06: ela é um plano feito com informação
  que a LEBRE não tem, e tornaria a tarefa trivial.
- Atribuições exigidas em qualquer material derivado: ONS (Dados Abertos); Open-Meteo e Copernicus Climate Change
  Service (ERA5); De Vito, S. (2008), UCI; NOAA National Ocean Service.
