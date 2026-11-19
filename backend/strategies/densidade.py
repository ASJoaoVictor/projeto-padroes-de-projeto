import pandas as pd

from .base import EstrategiaDistribuicao


class EstrategiaDensidade(EstrategiaDistribuicao):
    id = "densidade"
    nome = "Densidade demográfica"
    descricao = "Distribuição proporcional à densidade demográfica dos setores."
    criterio = "densidade_hab_km2"

    def pesos(self, regioes):
        return pd.to_numeric(regioes.get(self.criterio), errors="coerce").fillna(0).clip(lower=0)
