import { MapAdapter } from './MapAdapter.js';
export class GoogleMapsAdapter extends MapAdapter {
  async inicializar() { throw new Error('GoogleMapsAdapter é apenas um ponto de extensão; Google Maps ainda não foi integrado.'); }
}
