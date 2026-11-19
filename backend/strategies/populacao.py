import pandas as pd

from .base import EstrategiaDistribuicao


class EstrategiaPopulacao(EstrategiaDistribuicao):
    id = "populacao"
    nome = "População absoluta"
    descricao = "Distribuição proporcional à população residente no Censo 2022."
    criterio = "populacao_2022"

    def pesos(self, regioes):
        return pd.to_numeric(regioes.get(self.criterio), errors="coerce").fillna(0).clip(lower=0)
