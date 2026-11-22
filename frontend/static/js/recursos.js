export const RAIO_COBERTURA = 75;

export const CONFIG_RECURSOS = {
  viatura: {
    nome: 'Viatura policial',
    icone: new URL('../icons/viatura.svg', import.meta.url).href,
    cor: '#2563eb',
    raioCobertura: RAIO_COBERTURA,
  },
  ambulancia: {
    nome: 'Ambulância',
    icone: new URL('../icons/ambulancia.svg', import.meta.url).href,
    cor: '#16a34a',
    raioCobertura: RAIO_COBERTURA,
  },
};
