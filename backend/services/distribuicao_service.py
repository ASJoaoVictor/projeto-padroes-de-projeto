import math


def distribuir_maiores_restos(regioes, pesos, quantidade):
    """Aloca unidades inteiras pelo método de Hamilton (maiores restos).

    Empates são resolvidos pelo CD_SETOR em ordem crescente, garantindo que a
    mesma entrada produza sempre a mesma distribuição.
    """
    if quantidade < 0:
        raise ValueError("A quantidade não pode ser negativa.")
    resultado = {str(codigo): 0 for codigo in regioes["CD_SETOR"]}
    total_pesos = float(pesos.sum())
    if quantidade == 0 or total_pesos <= 0:
        return resultado

    cotas = pesos / total_pesos * quantidade
    bases = cotas.apply(math.floor).astype(int)
    for codigo, base in zip(regioes["CD_SETOR"], bases):
        resultado[str(codigo)] = int(base)

    restantes = quantidade - int(bases.sum())
    ordem = sorted(
        range(len(regioes)),
        key=lambda i: (-float(cotas.iloc[i] - bases.iloc[i]), str(regioes.iloc[i]["CD_SETOR"])),
    )
    for indice in ordem[:restantes]:
        resultado[str(regioes.iloc[indice]["CD_SETOR"])] += 1
    return resultado


class ServicoDistribuicao:
    def simular(self, regioes, estrategia, quantidade):
        pesos = estrategia.pesos(regioes)
        distribuicao = distribuir_maiores_restos(regioes, pesos, quantidade)
        elegiveis = int((pesos > 0).sum())
        avisos = []
        if quantidade and not elegiveis:
            avisos.append("Não há setores elegíveis para o critério selecionado.")
        if estrategia.id == "densidade":
            avisos.append("Densidade é um critério acadêmico simplificado e não representa necessidade operacional direta.")
        avisos.append("Marcadores representam recursos atribuídos aos setores, não localizações operacionais reais.")
        return distribuicao, elegiveis, avisos
