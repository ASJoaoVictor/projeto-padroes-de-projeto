import pandas as pd
import pytest

from app import create_app
from backend.routes.simulacoes import geografia


@pytest.fixture
def client():
    return create_app({"TESTING": True}).test_client()


def test_estrategias(client):
    resposta = client.get("/api/estrategias")
    assert resposta.status_code == 200
    estrategias = {item["id"]: item for item in resposta.get_json()}
    assert estrategias.keys() == {"densidade", "populacao", "area"}
    assert estrategias["area"]["nome"] == "Área territorial"
    assert estrategias["area"]["descricao"] == (
        "Distribui os recursos proporcionalmente à extensão territorial de cada setor censitário."
    )


def test_regioes_retorna_geojson_com_atributos(client):
    resposta = client.get("/api/regioes")
    corpo = resposta.get_json()
    assert resposta.status_code == 200
    assert corpo["type"] == "FeatureCollection"
    assert len(corpo["features"]) == 48
    assert corpo["features"][0]["geometry"] is not None
    assert "populacao_2022" in corpo["features"][0]["properties"]


def test_validacao_simulacao(client):
    resposta = client.post("/api/simulacoes", json={"tipo_recurso": "x", "quantidade": -1, "estrategia": "populacao"})
    assert resposta.status_code == 400


@pytest.mark.parametrize("estrategia", ["densidade", "populacao", "area"])
def test_simulacao_com_dados_de_picui(client, estrategia):
    resposta = client.post("/api/simulacoes", json={
        "tipo_recurso": "Viatura policial", "quantidade": 101, "estrategia": estrategia,
    })
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["estrategia"]["id"] == estrategia
    assert corpo["quantidade_distribuida"] == 101
    assert sum(item["quantidade"] for item in corpo["distribuicao"]) == 101


def test_simulacao_por_area_sem_setores_elegiveis(client, monkeypatch):
    setores = pd.DataFrame({"CD_SETOR": ["A"], "area_km2": [0]})
    monkeypatch.setattr(geografia, "setores", lambda: setores)
    resposta = client.post("/api/simulacoes", json={
        "tipo_recurso": "Ambulância", "quantidade": 2, "estrategia": "area",
    })
    assert resposta.status_code == 422
    assert "área territorial válida" in resposta.get_json()["erro"]["mensagem"]
