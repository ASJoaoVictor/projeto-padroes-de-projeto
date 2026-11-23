import pandas as pd

from .base import EstrategiaDistribuicao, SemSetoresElegiveis


class DistribuicaoPorArea(EstrategiaDistribuicao):
    id = "area"
    nome = "Área territorial"
    descricao = "Distribui os recursos proporcionalmente à extensão territorial de cada setor censitário."
    criterio = "area_km2"

    def pesos(self, regioes):
        areas = pd.to_numeric(
            regioes.get(self.criterio, pd.Series(index=regioes.index, dtype=float)),
            errors="coerce",
        )
        pesos = areas.where((areas > 0) & (areas < float("inf")), 0)
        if not pesos.gt(0).any():
            raise SemSetoresElegiveis("Não há setores com área territorial válida e positiva.")
        return pesos
