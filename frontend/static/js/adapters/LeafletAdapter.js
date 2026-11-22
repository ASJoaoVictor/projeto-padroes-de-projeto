import { MapAdapter } from './MapAdapter.js';

export class LeafletAdapter extends MapAdapter {
  async inicializar(elementoId, configuracoes = {}) {
    this.mapa = L.map(elementoId).setView(configuracoes.centro || [-6.51, -36.35], configuracoes.zoom || 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap' }).addTo(this.mapa);

    const cobertura = this.mapa.createPane('cobertura');
    cobertura.style.zIndex = '410';
    cobertura.style.pointerEvents = 'none';
    this.recursos = L.layerGroup().addTo(this.mapa);
  }

  desenharRegioes(geojson, opcoes) { this.regioes = L.geoJSON(geojson, { style: opcoes.estilo, onEachFeature: (f, l) => { l.bindPopup(opcoes.popup(f.properties)); l.on('click', () => l.setStyle({weight: 3, color: '#102a43'})); } }).addTo(this.mapa); }

  adicionarRecurso({posicao, setor, quantidade, configuracao}) {
    const latlng = L.GeoJSON.coordsToLatLng(posicao);
    const {nome, icone, cor, raioCobertura} = configuracao;
    const rotulo = `${nome} · setor ${setor} · quantidade ${quantidade}`;

    const imagem = document.createElement('img');
    imagem.src = icone;
    imagem.alt = '';
    const conteudo = document.createElement('div');
    conteudo.className = 'resource-symbol';
    conteudo.style.backgroundColor = cor;
    conteudo.append(imagem);

    if (quantidade > 1) {
      const badge = document.createElement('span');
      badge.className = 'resource-count';
      badge.textContent = quantidade;
      conteudo.append(badge);
    }

    const marcador = L.marker(latlng, {
      title: rotulo,
      icon: L.divIcon({className: 'resource-marker', html: conteudo, iconSize: [36, 36]}),
    });
    const popup = document.createElement('div');
    const titulo = document.createElement('strong');
    titulo.textContent = nome;
    popup.append(titulo, document.createElement('br'), `Setor: ${setor}`,
      document.createElement('br'), `Quantidade atribuída: ${quantidade}`);
    marcador.bindPopup(popup);

    const circulo = L.circle(latlng, {
      pane: 'cobertura',
      radius: raioCobertura,
      color: cor,
      weight: 2,
      fillOpacity: 0.16,
      interactive: false,
    });
    const grupo = L.layerGroup([circulo, marcador]).addTo(this.recursos);
    marcador.on('move', evento => circulo.setLatLng(evento.latlng));
    marcador.on('remove', () => grupo.removeLayer(circulo));
  }

  removerRecursos() { this.recursos?.clearLayers(); }
  atualizarEstiloRegioes(estilo) { this.regioes?.setStyle(feature => estilo(feature.properties)); }
  ajustarVisualizacao() { this.mapa.fitBounds(this.regioes.getBounds(), {padding: [18, 18]}); }
}
