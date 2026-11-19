from .densidade import EstrategiaDensidade
from .populacao import EstrategiaPopulacao

ESTRATEGIAS = {
    "densidade": EstrategiaDensidade(),
    "populacao": EstrategiaPopulacao(),
}
