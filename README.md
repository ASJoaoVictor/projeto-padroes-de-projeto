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

**Strategy.** `EstrategiaDistribuicao` define o contrato `pesos(regioes)`. Densidade demográfica, população absoluta e área territorial implementam esse contrato. Para adicionar um critério, defina `id`, `nome`, `descricao` e `criterio`, implemente `pesos` e registre uma instância em `backend/strategies/__init__.py`. O seletor carrega o catálogo de `GET /api/estrategias` e o `ServicoDistribuicao` aplica o método dos maiores restos.

**Adapter:** a interface depende de `MapAdapter`; `LeafletAdapter` traduz suas operações para Leaflet e conserva internamente as camadas concretas. `GoogleMapsAdapter` é somente um ponto de extensão e lança erro explícito até uma integração real ser criada.

Empates no método dos maiores restos são decididos pelo `CD_SETOR` crescente. Dados ausentes e valores não positivos são inelegíveis para o critério; a soma distribuída permanece igual à quantidade solicitada quando há setores elegíveis.
## Distribuição por área territorial

A estratégia `area` usa a coluna `area_km2` do GeoPackage. A cota de cada setor é sua área dividida pela soma das áreas válidas, multiplicada pelos recursos disponíveis. O serviço atribui primeiro a parte inteira das cotas e entrega as unidades restantes em ordem decrescente da parte fracionária. Com áreas de 10, 6 e 4 km² e 10 recursos, a alocação é de 5, 3 e 2 unidades.

Áreas ausentes, inválidas, infinitas ou não positivas têm peso zero. Se nenhum setor tiver área válida e positiva, `POST /api/simulacoes` retorna HTTP 422 com uma mensagem de erro.

A simulação usa apenas extensão territorial. Tempo de deslocamento, condições das estradas, distribuição espacial da população, demanda por atendimentos, disponibilidade operacional e sobreposição de coberturas ficam fora do cálculo. Os círculos de 2 km são ilustrações geométricas e não garantem cobertura integral dos setores.
