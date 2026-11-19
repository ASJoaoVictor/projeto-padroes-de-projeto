export class MapAdapter {
  async inicializar() { throw new Error('Adapter de mapa deve implementar inicializar.'); }
  desenharRegioes() { throw new Error('Adapter de mapa deve implementar desenharRegioes.'); }
  adicionarMarcador() { throw new Error('Adapter de mapa deve implementar adicionarMarcador.'); }
  limparMarcadores() { throw new Error('Adapter de mapa deve implementar limparMarcadores.'); }
  atualizarEstiloRegioes() { throw new Error('Adapter de mapa deve implementar atualizarEstiloRegioes.'); }
  ajustarVisualizacao() { throw new Error('Adapter de mapa deve implementar ajustarVisualizacao.'); }
}
