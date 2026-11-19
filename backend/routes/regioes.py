from flask import Blueprint, jsonify

from backend.services.geografia_service import ServicoGeografia
from backend.strategies import ESTRATEGIAS

bp = Blueprint("regioes", __name__, url_prefix="/api")
geografia = ServicoGeografia()


@bp.get("/regioes")
def listar_regioes():
    return jsonify(geografia.geojson())


@bp.get("/estrategias")
def listar_estrategias():
    return jsonify([{"id": e.id, "nome": e.nome, "descricao": e.descricao} for e in ESTRATEGIAS.values()])
