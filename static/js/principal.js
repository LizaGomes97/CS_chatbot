// Importações do Three.js
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

// Elementos do DOM
const balaoFala = document.getElementById("balao-fala");
const entradaUsuario = document.getElementById("entrada-usuario");
const formularioUsuario = document.getElementById("formulario-usuario");
const containerAvatar = document.getElementById("container-avatar");
const appData = document.getElementById("app-data");

// Obter dados do elemento HTML
const avatarUrl = appData.getAttribute("data-avatar-url");
const chatSessionId = appData.getAttribute("data-chat-session-id");

// Estado do chat
let nomeUsuario = "";
let conversaIniciada = false;

// Variáveis Three.js
let cena, camera, renderizador, modelo;
let mixer, relogio, acoes, acaoAtiva, acaoAnterior;
let rosto;

// Expressões disponíveis
const expressoes = ["Angry", "Surprised", "Sad", "Happy"];

// Estados de animação disponíveis
const estados = [
  "Idle",
  "Walking",
  "Running",
  "Dance",
  "Death",
  "Sitting",
  "Standing",
];

const emocoes = ["Jump", "Yes", "No", "Wave", "Punch", "ThumbsUp"];

// Inicialização
iniciarAvatar();

// Função para inicializar o avatar 3D
function iniciarAvatar() {
  // Configurar relogio para animações
  relogio = new THREE.Clock();

  // Criar cena
  cena = new THREE.Scene();
  cena.background = null; // Fundo transparente

  // Configurar câmera
  camera = new THREE.PerspectiveCamera(
    70,
    containerAvatar.clientWidth / containerAvatar.clientHeight,
    0.75,
    100
  );
  camera.position.set(0, 2, 4);
  camera.lookAt(0, 0, 0);

  // Configurar luzes
  const luzHemi = new THREE.HemisphereLight(0xffffff, 0x8d8d8d, 3);
  luzHemi.position.set(0, 20, 0);
  cena.add(luzHemi);

  const luzDir = new THREE.DirectionalLight(0xffffff, 3);
  luzDir.position.set(0, 10, 10);
  cena.add(luzDir);

  // Configurar renderizador
  renderizador = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderizador.setPixelRatio(window.devicePixelRatio);
  renderizador.setSize(
    containerAvatar.clientWidth,
    containerAvatar.clientHeight
  );
  renderizador.setClearColor(0x000000, 0); // Fundo transparente
  containerAvatar.appendChild(renderizador.domElement);

  // Carregar modelo do robô a partir da URL fornecida pelo Django
  const modelUrl = avatarUrl || "https://threejs.org/examples/models/gltf/RobotExpressive/RobotExpressive.glb";
  
  const carregador = new GLTFLoader();
  carregador.load(
    modelUrl,
    function (gltf) {
      modelo = gltf.scene;

      // Centralizar e escalar o modelo
      modelo.position.set(0, -1.5, 0);
      modelo.scale.set(0.9, 0.9, 0.9);

      // Adicionar à cena
      cena.add(modelo);

      // Configurar animações
      configurarAnimacoes(modelo, gltf.animations);

      // Ajustar a posição da câmera
      camera.lookAt(0, 1, 0);

      // Focar no campo de resposta após o carregamento
      setTimeout(() => {
        entradaUsuario.focus();
      }, 1000);
    },
    // Progresso do carregamento
    function (xhr) {
      console.log((xhr.loaded / xhr.total) * 100 + '% carregado');
    },
    // Erro no carregamento
    function (error) {
      console.error('Erro ao carregar o modelo:', error);
    }
  );

  // Evento de redimensionamento
  window.addEventListener("resize", aoRedimensionarJanela);

  // Iniciar loop de animação
  animar();
}

// Configurar animações do modelo
function configurarAnimacoes(modelo, animacoes) {
  mixer = new THREE.AnimationMixer(modelo);
  acoes = {};

  for (let i = 0; i < animacoes.length; i++) {
    const clip = animacoes[i];
    const acao = mixer.clipAction(clip);
    acoes[clip.name] = acao;

    if (emocoes.indexOf(clip.name) >= 0 || estados.indexOf(clip.name) >= 4) {
      acao.clampWhenFinished = true;
      acao.loop = THREE.LoopOnce;
    }
  }

  // Encontrar rosto para expressões
  rosto = modelo.getObjectByName("Head_4");

  // Iniciar com Idle
  mudarParaAcao("Idle", 0.5);
}

// Mudar animação com transição suave
function mudarParaAcao(nome, duracao) {
  // Verificar se a ação existe
  if (!acoes[nome]) {
    console.warn(`Animação "${nome}" não encontrada. Usando "Idle" como padrão.`);
    nome = "Idle"; // Fallback para Idle se a animação solicitada não existir
    
    // Se ainda não existir Idle, não faz nada
    if (!acoes[nome]) {
      console.error("Animação padrão 'Idle' também não encontrada.");
      return;
    }
  }
  
  acaoAnterior = acaoAtiva;
  acaoAtiva = acoes[nome];

  if (acaoAnterior !== acaoAtiva) {
    if (acaoAnterior) acaoAnterior.fadeOut(duracao);
  }

  acaoAtiva
    .reset()
    .setEffectiveTimeScale(1)
    .setEffectiveWeight(1)
    .fadeIn(duracao)
    .play();
}

// Função para definir expressão facial
function definirExpressao(nome, valor = 1) {
  if (!rosto || !rosto.morphTargetDictionary) {
    return;
  }
  
  // Se o nome da expressão não for fornecido, reseta todas as expressões
  if (!nome) {
    for (let i = 0; i < rosto.morphTargetInfluences.length; i++) {
      rosto.morphTargetInfluences[i] = 0;
    }
    return;
  }
  
  const indice = rosto.morphTargetDictionary[nome];
  if (indice !== undefined) {
    // Resetar todas as expressões
    for (let i = 0; i < rosto.morphTargetInfluences.length; i++) {
      rosto.morphTargetInfluences[i] = 0;
    }
    // Definir nova expressão
    rosto.morphTargetInfluences[indice] = valor;
  } else {
    console.warn(`Expressão "${nome}" não encontrada.`);
  }
}

// Redimensionar ao alterar tamanho da janela
function aoRedimensionarJanela() {
  camera.aspect = containerAvatar.clientWidth / containerAvatar.clientHeight;
  camera.updateProjectionMatrix();
  renderizador.setSize(
    containerAvatar.clientWidth,
    containerAvatar.clientHeight
  );
}

// Loop de animação
function animar() {
  requestAnimationFrame(animar);

  if (mixer) {
    mixer.update(relogio.getDelta());
  }

  renderizador.render(cena, camera);
}

// Exportar funções e variáveis para uso em outros módulos
export {
  mudarParaAcao,
  definirExpressao,
  expressoes,
  estados,
  emocoes,
  nomeUsuario,
  conversaIniciada,
  entradaUsuario,
  formularioUsuario,
  chatSessionId
};