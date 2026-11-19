import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app({"TESTING": True}).test_client()


def test_estrategias(client):
    resposta = client.get("/api/estrategias")
    assert resposta.status_code == 200
    assert {x["id"] for x in resposta.get_json()} == {"densidade", "populacao"}


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
