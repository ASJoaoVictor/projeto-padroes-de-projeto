# GeoDistribuição — Picuí/PB

Simulador acadêmico de distribuição proporcional de recursos entre os setores censitários de Picuí. Usa dados do **IBGE, Censo Demográfico 2022** e não representa despacho operacional nem localização real de recursos.

## Executar

Requer Python 3.12+ e o GeoPackage original em `../picui_setores.gpkg` (já referenciado pelo projeto) ou em `dados/picui_setores.gpkg`.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Acesse `http://127.0.0.1:5000`. Para executar os testes: `pytest`.

## Padrões de projeto

**Strategy:** `EstrategiaDistribuicao` define o contrato de pesos; `EstrategiaDensidade` e `EstrategiaPopulacao` são estratégias independentes, registradas centralmente em `backend/strategies/__init__.py`. `ServicoDistribuicao` mantém o algoritmo matemático (maiores restos) fora dessas classes. Para incluir um critério, implemente o contrato e registre-o.

**Adapter:** a interface depende de `MapAdapter`; `LeafletAdapter` traduz suas operações para Leaflet e conserva internamente as camadas concretas. `GoogleMapsAdapter` é somente um ponto de extensão e lança erro explícito até uma integração real ser criada.

Empates no método dos maiores restos são decididos pelo `CD_SETOR` crescente. Dados ausentes e valores não positivos são inelegíveis para o critério; a soma distribuída permanece igual à quantidade solicitada quando há setores elegíveis.
# projeto-padroes-de-projeto
