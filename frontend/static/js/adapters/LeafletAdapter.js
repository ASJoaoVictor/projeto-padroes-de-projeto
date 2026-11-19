import { MapAdapter } from './MapAdapter.js';

export class LeafletAdapter extends MapAdapter {
  async inicializar(elementoId, configuracoes = {}) { this.mapa = L.map(elementoId).setView(configuracoes.centro || [-6.51, -36.35], configuracoes.zoom || 12); L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap' }).addTo(this.mapa); this.marcadores = L.layerGroup().addTo(this.mapa); }
  desenharRegioes(geojson, opcoes) { this.regioes = L.geoJSON(geojson, { style: opcoes.estilo, onEachFeature: (f, l) => { l.bindPopup(opcoes.popup(f.properties)); l.on('click', () => l.setStyle({weight: 3, color: '#102a43'})); } }).addTo(this.mapa); }
  adicionarMarcador({latlng, texto, popup}) { L.marker(latlng, { icon: L.divIcon({className: 'resource-marker', html: texto, iconSize: [30, 30]}) }).bindPopup(popup).addTo(this.marcadores); }
  limparMarcadores() { this.marcadores.clearLayers(); }
  atualizarEstiloRegioes(estilo) { this.regioes.setStyle(feature => estilo(feature.properties)); }
  ajustarVisualizacao() { this.mapa.fitBounds(this.regioes.getBounds(), {padding: [18, 18]}); }
  centroide(feature) { return this.regioes.getLayers().find(l => String(l.feature.properties.CD_SETOR) === String(feature.properties.CD_SETOR)).getBounds().getCenter(); }
}
