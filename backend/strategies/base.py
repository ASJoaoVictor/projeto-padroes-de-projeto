from abc import ABC, abstractmethod


class EstrategiaDistribuicao(ABC):
    """Contrato Strategy: cada critério entrega pesos por setor."""

    id: str
    nome: str
    descricao: str
    criterio: str

    @abstractmethod
    def pesos(self, regioes):
        """Retorna pesos numéricos, um por região, ou zero para inelegível."""
