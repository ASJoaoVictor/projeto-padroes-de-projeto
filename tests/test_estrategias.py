import pandas as pd

from backend.services.distribuicao_service import distribuir_maiores_restos
from backend.strategies.populacao import EstrategiaPopulacao


def regioes(populacoes):
    return pd.DataFrame({"CD_SETOR": [f"s{i}" for i in range(len(populacoes))], "populacao_2022": populacoes, "densidade_hab_km2": populacoes})


def test_maiores_restos_soma_e_proporcao():
    r = regioes([10, 20, 30]); d = distribuir_maiores_restos(r, EstrategiaPopulacao().pesos(r), 10)
    assert d == {"s0": 2, "s1": 3, "s2": 5}


def test_zero_ausente_empate_e_determinismo():
    r = regioes([0, None, 1, 1]); p = EstrategiaPopulacao().pesos(r)
    assert distribuir_maiores_restos(r, p, 0) == {"s0": 0, "s1": 0, "s2": 0, "s3": 0}
    assert distribuir_maiores_restos(r, p, 1) == {"s0": 0, "s1": 0, "s2": 1, "s3": 0}
    assert sum(distribuir_maiores_restos(r, p, 9).values()) == 9
