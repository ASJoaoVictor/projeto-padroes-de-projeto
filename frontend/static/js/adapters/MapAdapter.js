export class MapAdapter {
  async inicializar() { throw new Error('Adapter de mapa deve implementar inicializar.'); }
  desenharRegioes() { throw new Error('Adapter de mapa deve implementar desenharRegioes.'); }
  atualizarEstiloRegioes() { throw new Error('Adapter de mapa deve implementar atualizarEstiloRegioes.'); }
  ajustarVisualizacao() { throw new Error('Adapter de mapa deve implementar ajustarVisualizacao.'); }

  // Cada recurso contém configuração visual, código do setor, quantidade e posição [longitude, latitude].
  atualizarRecursos(recursos) {
    this.removerRecursos();
    recursos.forEach(recurso => this.adicionarRecurso(recurso));
  }

  adicionarRecurso() { throw new Error('Adapter de mapa deve implementar adicionarRecurso.'); }
  removerRecursos() { throw new Error('Adapter de mapa deve implementar removerRecursos.'); }
}
