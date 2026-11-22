import { LeafletAdapter } from './adapters/LeafletAdapter.js';
import { CONFIG_RECURSOS, RAIO_COBERTURA } from './recursos.js';
import { api } from './services/api.js';

const mapa = new LeafletAdapter(); let geojson; let indicador = 'densidade_hab_km2';
const form = document.getElementById('form-simulacao');
let versaoSimulacao = 0;
const fmt = new Intl.NumberFormat('pt-BR', {maximumFractionDigits: 1});
const el = id => document.getElementById(id);
function valor(p) { return Number(p[indicador]) || 0; }
function escala(v, max) { if (!v) return '#cbd5e1'; const t = max ? v/max : 0; return `hsl(${205 - Math.min(t,1)*170} 68% ${72-Math.min(t,1)*25}%)`; }
function estilo(p) { const max = Math.max(...geojson.features.map(f => valor(f.properties))); return {color:'#fff', weight:1, fillColor:escala(valor(p),max), fillOpacity:.82}; }
function popup(p) { return `<strong>Setor censitário</strong><br>Código: ${p.CD_SETOR}<br>População: ${fmt.format(p.populacao_2022 ?? 0)}<br>Área: ${fmt.format(p.area_km2 ?? 0)} km²<br>Densidade: ${fmt.format(p.densidade_hab_km2 ?? 0)} hab/km²`; }
function legenda() { const vals=geojson.features.map(f=>valor(f.properties)).filter(Boolean), max=Math.max(...vals,0); el('legenda').innerHTML=`<strong>${indicador === 'populacao_2022'?'População (hab.)':'Densidade (hab./km²)'}</strong><div><i style="background:#cbd5e1"></i>Sem dados ou zero</div><div><i style="background:${escala(max*.35,max)}"></i>até ${fmt.format(max*.5)}</div><div><i style="background:${escala(max,max)}"></i>até ${fmt.format(max)}</div>`; }
function atualizarMapa() { mapa.atualizarEstiloRegioes(estilo); legenda(); }
async function iniciar() { try { const [dados, estrategias] = await Promise.all([api.regioes(), api.estrategias()]); geojson=dados; await mapa.inicializar('mapa'); mapa.desenharRegioes(geojson,{estilo: f=>estilo(f.properties),popup}); mapa.ajustarVisualizacao(); estrategias.forEach(e=>el('estrategia').add(new Option(e.nome,e.id))); legenda(); el('executar').disabled = false; el('estado').textContent=`${dados.metadata.quantidade_setores} setores censitários carregados.`; } catch(e) { el('estado').textContent=e.message; } }
el('indicador').addEventListener('change', e=>{indicador=e.target.value; atualizarMapa();});
function configurarSelecao() {
  const botoes = Object.entries(CONFIG_RECURSOS).map(([tipo, recurso]) => {
    const botao = document.createElement('button');
    botao.type = 'button';
    botao.className = 'resource-option';
    botao.dataset.tipo = tipo;
    botao.style.setProperty('--resource-color', recurso.cor);

    const imagem = document.createElement('img');
    imagem.src = recurso.icone;
    imagem.alt = '';
    botao.append(imagem, recurso.nome);
    botao.addEventListener('click', () => selecionar(tipo));
    return botao;
  });

  function selecionar(tipo) {
    form.elements.tipo_recurso.value = CONFIG_RECURSOS[tipo].nome;
    botoes.forEach(botao => botao.setAttribute('aria-pressed', botao.dataset.tipo === tipo));
  }

  el('tipos-recursos').append(...botoes);
  selecionar(botoes[0].dataset.tipo);
  el('raio-cobertura').textContent = `${fmt.format(RAIO_COBERTURA / 1000)} km`;
}

function limparResultado() {
  mapa.removerRecursos();
  for (const id of ['resumo', 'avisos', 'distribuicao']) el(id).replaceChildren();
}

el('limpar').addEventListener('click', () => {
  versaoSimulacao++;
  limparResultado();
  el('estado').textContent = 'Simulação removida.';
});

form.addEventListener('submit', async evento => {
  evento.preventDefault();
  if (el('executar').disabled) return;

  const versao = ++versaoSimulacao;
  const dados = Object.fromEntries(new FormData(form));
  dados.quantidade = Number(dados.quantidade);
  const configuracao = Object.values(CONFIG_RECURSOS).find(recurso => recurso.nome === dados.tipo_recurso);
  limparResultado();
  el('estado').textContent = 'Executando simulação…';

  try {
    const r = await api.simular(dados);
    if (versao !== versaoSimulacao) return;

    const porSetor = new Map(r.distribuicao.map(item => [item.cd_setor, item.quantidade]));
    const recursos = [];
    for (const {properties} of geojson.features) {
      const setor = String(properties.CD_SETOR);
      const quantidade = porSetor.get(setor);
      const posicao = properties.ponto_representativo;
      if (quantidade > 0 && posicao) recursos.push({setor, quantidade, posicao, configuracao});
    }
    mapa.atualizarRecursos(recursos);

    el('estado').textContent = `Simulação por ${r.estrategia.nome.toLowerCase()} concluída.`;
    el('resumo').innerHTML = `<dl><dt>Solicitados</dt><dd>${r.quantidade_solicitada}</dd><dt>Distribuídos</dt><dd>${r.quantidade_distribuida}</dd><dt>Setores analisados</dt><dd>${r.regioes_analisadas}</dd><dt>Contemplados</dt><dd>${r.regioes_contempladas}</dd></dl>`;
    el('avisos').innerHTML = r.avisos.map(a => `<p class="warning">${a}</p>`).join('');
    el('distribuicao').innerHTML = r.distribuicao
      .filter(x => x.quantidade)
      .sort((a, b) => b.quantidade - a.quantidade || a.cd_setor.localeCompare(b.cd_setor))
      .map(x => `<li><code>${x.cd_setor}</code><b>${x.quantidade}</b></li>`).join('') || '<li>Nenhum setor contemplado.</li>';
  } catch (erro) {
    if (versao === versaoSimulacao) el('estado').textContent = erro.message;
  }
});

configurarSelecao();
iniciar();
