from pathlib import Path

import geopandas as gpd
import pandas as pd


class RepositorioSetores:
    """Carrega a base real uma vez e a mantém em memória durante o processo."""

    CAMPOS = ["CD_SETOR", "CD_MUN", "NM_MUN", "SITUACAO", "populacao_2022", "area_km2", "densidade_hab_km2"]

    def __init__(self, caminho=None):
        raiz = Path(__file__).resolve().parents[2]
        candidatos = [raiz / "dados" / "picui_setores.gpkg", raiz.parent / "picui_setores.gpkg"]
        self.caminho = Path(caminho) if caminho else next((p for p in candidatos if p.exists()), candidatos[0])
        self._setores = None

    def obter(self):
        if self._setores is None:
            if not self.caminho.exists():
                raise FileNotFoundError(f"GeoPackage não encontrado: {self.caminho}")
            setores = gpd.read_file(self.caminho, engine="pyogrio")
            faltantes = {"CD_SETOR", "populacao_2022", "area_km2"} - set(setores.columns)
            if faltantes:
                raise ValueError(f"GeoPackage sem campos obrigatórios: {', '.join(sorted(faltantes))}")
            if setores.crs is None:
                raise ValueError("GeoPackage sem sistema de coordenadas definido.")
            setores = setores.to_crs("EPSG:4326")
            if "densidade_hab_km2" not in setores:
                area = pd.to_numeric(setores["area_km2"], errors="coerce")
                pop = pd.to_numeric(setores["populacao_2022"], errors="coerce")
                setores["densidade_hab_km2"] = pop / area.where(area > 0)
            self._setores = setores
        return self._setores.copy()
