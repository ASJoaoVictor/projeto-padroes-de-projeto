from abc import ABC, abstractmethod


class SemSetoresElegiveis(ValueError):
    """O critério selecionado não encontrou setores elegíveis."""


class EstrategiaDistribuicao(ABC):
    """Contrato Strategy: cada critério entrega pesos por setor."""

    id: str
    nome: str
    descricao: str
    criterio: str

    @abstractmethod
    def pesos(self, regioes):
        """Retorna pesos numéricos, um por região, ou zero para inelegível."""
