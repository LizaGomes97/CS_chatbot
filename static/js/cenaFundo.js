// Importações do Three.js
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { TexturePass } from "three/addons/postprocessing/TexturePass.js";
import { CubeTexturePass } from "three/addons/postprocessing/CubeTexturePass.js";
import { ClearPass } from "three/addons/postprocessing/ClearPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

// Elementos do DOM
const cenaFundo = document.getElementById("cena-fundo");

// Variáveis Three.js para o fundo com a arma
let cenaFundoRend, cameraFundo, rendFundo, composerFundo;
let arma, controleFundo;
let passagemClear, passagemTextura, passagemRender, passagemCubeTextura;

// Configurações do fundo
const configFundo = {
  passagemClear: true,
  corDeFundo: "white",
  alphaDeFundo: 1.0,
  passagemTextura: true,
  opacidadeTextura: 0.3,
  passagemCubeTextura: true,
  opacidadeCubeTextura: 10,
  passagemRender: true,
};

// Inicialização
iniciarCenaFundo();

// Função para inicializar a cena de fundo com a arma
function iniciarCenaFundo() {
  // Verificar se o elemento canvas existe
  if (!cenaFundo) {
    console.error("Elemento canvas para cena de fundo não encontrado!");
    return;
  }

  // IMPORTANTE: Configurar o estilo do canvas diretamente
  cenaFundo.style.position = 'fixed';
  cenaFundo.style.top = `calc(-9vh)`;
  cenaFundo.style.left = `calc(-37vw)`;
  cenaFundo.style.width = '100vw';
  cenaFundo.style.height = '100vh';
  cenaFundo.style.zIndex = '-10';
  cenaFundo.style.pointerEvents = 'none';

  // Criar cena
  cenaFundoRend = new THREE.Scene();

  // Configurar câmera com um campo de visão mais amplo
  cameraFundo = new THREE.PerspectiveCamera(
    70, // Campo de visão mais amplo para mostrar mais da cena
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  cameraFundo.position.z = 10; // Afastar um pouco para mostrar mais da cena

  // Configurar renderizador
  rendFundo = new THREE.WebGLRenderer({
    canvas: cenaFundo,
    antialias: true,
    alpha: true,
    premultipliedAlpha: false, // Melhora a transparência
  });
  rendFundo.setPixelRatio(window.devicePixelRatio);
  
  // IMPORTANTE: Definir o tamanho para toda a janela
  rendFundo.setSize(window.innerWidth, window.innerHeight);
  
  // Garantir fundo transparente
  rendFundo.setClearColor(0x000000, 0);

  // Adicionar luzes
  const luz1 = new THREE.PointLight(0xefffef, 500);
  luz1.position.set(-10, -10, 10);
  cenaFundoRend.add(luz1);

  const luz2 = new THREE.PointLight(0xffefef, 500);
  luz2.position.set(-10, 10, 10);
  cenaFundoRend.add(luz2);

  const luz3 = new THREE.PointLight(0xefefff, 500);
  luz3.position.set(10, -10, 10);
  cenaFundoRend.add(luz3);

  // Grupo para arma
  const grupo = new THREE.Group();
  cenaFundoRend.add(grupo);

  // Carregar o modelo da arma
  const carregadorArma = new GLTFLoader();
  carregadorArma.load(
    "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/models/gltf/Cerberus/Cerberus.glb",
    function (gltf) {
      arma = gltf.scene;

      // Ajustar a posição e escala da arma
      arma.scale.set(0.8, 0.8, 0.8); // Aumentar um pouco a escala
      arma.position.set(0, 0, 0);
      arma.rotation.y = Math.PI / 4;

      // Adicionar à cena
      grupo.add(arma);
    },
    // Função de progresso
    function (xhr) {
      console.log((xhr.loaded / xhr.total * 100) + '% carregado');
    },
    // Função de erro
    function (error) {
      console.error('Erro ao carregar modelo da arma:', error);
    }
  );

  // Configurar pós-processamento
  // Função para gerar URLs de cubemap
  const gerarUrlsCube = function (prefixo, sufixo) {
    return [
      prefixo + "px" + sufixo,
      prefixo + "nx" + sufixo,
      prefixo + "py" + sufixo,
      prefixo + "ny" + sufixo,
      prefixo + "pz" + sufixo,
      prefixo + "nz" + sufixo,
    ];
  };

  // Criar composer
  composerFundo = new EffectComposer(rendFundo);

  // Adicionar ClearPass
  passagemClear = new ClearPass(
    definirCorFundo(configFundo.corDeFundo),
    configFundo.alphaDeFundo
  );
  composerFundo.addPass(passagemClear);

  // Adicionar TexturePass
  passagemTextura = new TexturePass();
  composerFundo.addPass(passagemTextura);

  // Carregar cubemap e adicionar CubeTexturePass
  const urlsLdr = gerarUrlsCube(
    "https://threejs.org/examples/textures/cube/pisa/",
    ".png"
  );
  new THREE.CubeTextureLoader().load(urlsLdr, function (ldrCubeMap) {
    passagemCubeTextura = new CubeTexturePass(cameraFundo, ldrCubeMap);
    passagemCubeTextura.opacity = configFundo.opacidadeCubeTextura;
    composerFundo.insertPass(passagemCubeTextura, 2);
  });

  // Adicionar RenderPass
  passagemRender = new RenderPass(cenaFundoRend, cameraFundo);
  passagemRender.clear = false;
  composerFundo.addPass(passagemRender);

  // Adicionar OutputPass
  const passagemOutput = new OutputPass();
  composerFundo.addPass(passagemOutput);

  // Controles de órbita
  controleFundo = new OrbitControls(cameraFundo, rendFundo.domElement);
  controleFundo.enableDamping = true;
  controleFundo.dampingFactor = 0.05;
  controleFundo.screenSpacePanning = false;
  controleFundo.maxPolarAngle = Math.PI / 2;
  controleFundo.enableZoom = false;
  controleFundo.autoRotate = true; // Ativar rotação automática
  controleFundo.autoRotateSpeed = 0.5; // Reduzir velocidade para não distrair

  // Evento de redimensionamento
  window.addEventListener("resize", redimensionarCenaFundo);

  // Iniciar loop de animação
  animarCenaFundo();
}

// Função para obter código de cor baseado no nome
function definirCorFundo(cor) {
  switch (cor) {
    case "blue":
      return 0x0000ff;
    case "red":
      return 0xff0000;
    case "green":
      return 0x00ff00;
    case "white":
      return 0xffffff;
    case "black":
      return 0x000000;
    default:
      return 0x0000ff;
  }
}

// Redimensionar - IMPORTANTE: Usar dimensões da janela
function redimensionarCenaFundo() {
  if (!cenaFundo) return;
  
  cameraFundo.aspect = window.innerWidth / window.innerHeight;
  cameraFundo.updateProjectionMatrix();
  
  // Usar as dimensões da janela, não do container
  rendFundo.setSize(window.innerWidth, window.innerHeight);
  composerFundo.setSize(window.innerWidth, window.innerHeight);
}

// Loop de animação para cena de fundo
function animarCenaFundo() {
  requestAnimationFrame(animarCenaFundo);

  if (controleFundo) {
    controleFundo.update();
  }

  // Atualizar passagens de renderização
  if (passagemClear) {
    passagemClear.enabled = configFundo.passagemClear;
    passagemClear.clearAlpha = configFundo.alphaDeFundo;
  }

  if (passagemTextura) {
    passagemTextura.enabled = configFundo.passagemTextura;
    passagemTextura.opacity = configFundo.opacidadeTextura;
  }

  if (passagemCubeTextura) {
    passagemCubeTextura.enabled = configFundo.passagemCubeTextura;
    passagemCubeTextura.opacity = configFundo.opacidadeCubeTextura;
  }

  if (passagemRender) {
    passagemRender.enabled = configFundo.passagemRender;
  }

  // Animar arma
  if (arma) {
    arma.rotation.y += 0.005;
  }

  // Renderizar com o composer
  composerFundo.render();
}