"""Montagem de séries reais e critério padrão da Frente B."""
import numpy as np
import pandas as pd


def serie(nome, alvo, entradas, grupo=None, season=None, season2=None, freq="h"):
    """Alinha alvo e entradas numa grade completa de frequência `freq` (lacunas viram NaN).

    freq=None mantém o calendário do próprio alvo (ex. dias úteis ou meses já montados pelo cenário).
    """
    ini, fim = max(alvo.index.min(), entradas.index.min()), min(alvo.index.max(), entradas.index.max())
    if freq is None:
        idx = alvo.index[(alvo.index >= ini) & (alvo.index <= fim)]
    else:
        idx = pd.date_range(ini, fim, freq=freq)
    a = alvo[~alvo.index.duplicated()].reindex(idx)
    e = entradas[~entradas.index.duplicated()].reindex(idx)
    return dict(nome=nome, grupo=grupo or nome, y=a.to_numpy(float), X=e.to_numpy(float), season=season, season2=season2,
                entradas=list(e.columns), inicio=str(idx[0]), fim=str(idx[-1]))


def vento_uv(vel, dire):
    """Componentes u (leste) e v (norte) do vento a partir da velocidade e da direção de onde ele vem (graus)."""
    r = np.deg2rad(dire)
    return -vel * np.sin(r), -vel * np.cos(r)


def aceitas(r):
    """Nomes reais das entradas aceitas numa série (x0 -> nome da coluna)."""
    nomes = r.get("entradas") or []
    out = set()
    for e in r["eventos"]:
        if e["resultado"] == "accepted" and e["entra"]:
            u = e["entra"].split("[")[0]
            if u.startswith("x") and u[1:].isdigit() and int(u[1:]) < len(nomes):
                out.add(nomes[int(u[1:])])
            else:
                out.add(u)
    return sorted(out)


def criterio_padrao(resumo, series, ref):
    """Critério comum aos cenários reais, declarado no PLANO e repetido em cada cenário:
    (1) MSE relativo ao comparador de referência `ref` (média geométrica) < 1;
    (2) MSE relativo ao linear online (média geométrica) <= 1,05;
    (3) cobertura média do intervalo de 90% entre 0,85 e 0,95.
    """
    resumo["entradas_aceitas"] = {r["nome"]: aceitas(r) for r in series}
    resumo["mse_rel_por_serie"] = {r["nome"]: {k[8:]: round(v, 3) for k, v in r.items() if k.startswith("mse_rel_")}
                                   for r in series}
    c1 = resumo[f"mse_rel_{ref}_geo"] < 1
    c2 = resumo["mse_rel_linear_online_geo"] <= 1.05
    c3 = 0.85 <= resumo["cobertura_media"] <= 0.95
    resumo["partes_do_criterio"] = dict(vence_referencia=bool(c1), empata_ou_vence_linear=bool(c2), cobertura_ok=bool(c3))
    return "atende" if c1 and c2 and c3 else "nao_atende"


def criterio_nulo(resumo, series, ref, tol=1.02, max_series_com_falsa=1):
    """Critério dos testes negativos (nada externo a descobrir):
    (1) MSE relativo ao comparador `ref` (média geométrica) <= tol (não piora a previsão trivial);
    (2) no máximo `max_series_com_falsa` séries com alguma entrada externa aceita (o próprio passado não conta).
    """
    resumo["entradas_aceitas"] = {r["nome"]: aceitas(r) for r in series}
    resumo["mse_rel_por_serie"] = {r["nome"]: {k[8:]: round(v, 3) for k, v in r.items() if k.startswith("mse_rel_")}
                                   for r in series}
    c1 = resumo[f"mse_rel_{ref}_geo"] <= tol
    c2 = resumo["series_com_falsa"] <= max_series_com_falsa
    resumo["partes_do_criterio"] = dict(nao_piora_referencia=bool(c1), sem_espurias=bool(c2))
    return "atende" if c1 and c2 else "nao_atende"
