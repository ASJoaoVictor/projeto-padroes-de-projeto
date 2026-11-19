import json
import math

from backend.repositories.setores_repository import RepositorioSetores


def _valor_json(valor):
    try:
        return None if valor is None or math.isnan(float(valor)) else valor
    except (TypeError, ValueError):
        return valor


class ServicoGeografia:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio or RepositorioSetores()

    def setores(self):
        return self.repositorio.obter()

    def geojson(self):
        setores = self.setores()
        campos = [c for c in self.repositorio.CAMPOS if c in setores.columns]
        features = []
        for _, setor in setores.iterrows():
            propriedades = {campo: _valor_json(setor[campo]) for campo in campos}
            features.append({"type": "Feature", "properties": propriedades, "geometry": setor.geometry.__geo_interface__})
        return {"type": "FeatureCollection", "features": features, "metadata": {"fonte": "IBGE, Censo Demográfico 2022", "quantidade_setores": len(features), "crs": "EPSG:4326"}}
