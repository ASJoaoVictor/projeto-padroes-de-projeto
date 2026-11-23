from flask import Blueprint, jsonify, request

from backend.routes.regioes import geografia
from backend.services.distribuicao_service import ServicoDistribuicao
from backend.strategies import ESTRATEGIAS
from backend.strategies.base import SemSetoresElegiveis

bp = Blueprint("simulacoes", __name__, url_prefix="/api")


def erro(mensagem, status=400):
    return jsonify({"erro": {"mensagem": mensagem}}), status


@bp.post("/simulacoes")
def criar_simulacao():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return erro("Envie um objeto JSON válido.")
    tipo = dados.get("tipo_recurso")
    estrategia_id = dados.get("estrategia")
    quantidade = dados.get("quantidade")
    if not isinstance(tipo, str) or not tipo.strip():
        return erro("tipo_recurso é obrigatório.")
    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade < 0:
        return erro("quantidade deve ser um inteiro não negativo.")
    estrategia = ESTRATEGIAS.get(estrategia_id)
    if not estrategia:
        return erro("Estratégia inválida.")
    try:
        setores = geografia.setores()
        distribuicao, elegiveis, avisos = ServicoDistribuicao().simular(setores, estrategia, quantidade)
    except SemSetoresElegiveis as exc:
        return erro(str(exc), 422)
    except (FileNotFoundError, ValueError) as exc:
        return erro(str(exc), 503)
    itens = [{"cd_setor": codigo, "quantidade": valor} for codigo, valor in distribuicao.items()]
    return jsonify({"estrategia": {"id": estrategia.id, "nome": estrategia.nome, "criterio": estrategia.criterio}, "tipo_recurso": tipo.strip(), "quantidade_solicitada": quantidade, "quantidade_distribuida": sum(distribuicao.values()), "regioes_analisadas": len(setores), "regioes_elegiveis": elegiveis, "regioes_contempladas": sum(valor > 0 for valor in distribuicao.values()), "distribuicao": itens, "avisos": avisos})
