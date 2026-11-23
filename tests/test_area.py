import pandas as pd
import pytest

from backend.services.distribuicao_service import ServicoDistribuicao
from backend.strategies import ESTRATEGIAS
from backend.strategies.base import SemSetoresElegiveis


@pytest.mark.parametrize(
    ("areas", "quantidade", "esperado"),
    [
        ([10, 6, 4], 10, [5, 3, 2]),
        ([10, 6, 4], 7, [4, 2, 1]),
        ([10, 6, 4], 0, [0, 0, 0]),
        ([1, 1, 1], 1, [0, 1, 0]),
        ([1, 1, 1], 2, [0, 1, 1]),
        ([1, 1, 1], 5, [1, 2, 2]),
        ([1, 1, 100000], 20, [0, 0, 20]),
        ([0, "2", None], 6, [0, 6, 0]),
        (["inválida", -1, 2], 6, [0, 0, 6]),
        ([float("inf"), float("nan"), 2], 6, [0, 0, 6]),
    ],
)
def test_simulacao_por_area(areas, quantidade, esperado):
    setores = pd.DataFrame({
        "CD_SETOR": ["C", "A", "B"],
        "area_km2": areas,
        "populacao_2022": [200, 10, 90],
        "densidade_hab_km2": [50, 300, 70],
    })
    servico = ServicoDistribuicao()
    resultado, _, _ = servico.simular(setores, ESTRATEGIAS["area"], quantidade)
    assert resultado == dict(zip(setores["CD_SETOR"], esperado))
    assert sum(resultado.values()) == quantidade
    assert servico.simular(setores.iloc[::-1], ESTRATEGIAS["area"], quantidade)[0] == resultado


@pytest.mark.parametrize("campos", [{}, {"area_km2": [0, None]}])
def test_area_sem_setores_elegiveis(campos):
    setores = pd.DataFrame({"CD_SETOR": ["A", "B"], **campos})
    with pytest.raises(SemSetoresElegiveis, match="área territorial válida"):
        ServicoDistribuicao().simular(setores, ESTRATEGIAS["area"], 1)
