// Elementos do HUD
let dinheiroElemento;
let vidaElemento;
let tempoElemento;
let municaoPrimariaElemento;
let municaoReservaElemento;

// Obter dados do elemento de dados da aplicação
const appData = document.getElementById("app-data");

// Valores iniciais do HUD (obtidos dos atributos data do elemento)
let dinheiro = parseInt(appData.getAttribute("data-hud-initial-money") || 7000);
let vida = parseInt(appData.getAttribute("data-hud-initial-health") || 100);
let tempoRestante = parseInt(appData.getAttribute("data-hud-round-time") || 105); // 1:45 em segundos
let municaoPrimaria = parseInt(appData.getAttribute("data-hud-initial-ammo-primary") || 30);
let municaoReserva = parseInt(appData.getAttribute("data-hud-initial-ammo-reserve") || 90);
let mostrarInstrucoes = (appData.getAttribute("data-hud-show-instructions") || "true") === "true";

// Inicializar HUD
function inicializarHUD() {
  // Obter referências aos elementos
  dinheiroElemento = document.querySelector(".dinheiro");
  vidaElemento = document.querySelector(".vida");
  tempoElemento = document.querySelector(".tempo");
  municaoPrimariaElemento = document.querySelector(".municao-primaria");
  municaoReservaElemento = document.querySelector(".municao-reserva");

  // Atualizar valores iniciais
  atualizarHUD();

  // Iniciar contador de tempo
  setInterval(atualizarTempo, 1000);
}

// Atualizar todos os elementos do HUD
function atualizarHUD() {
  // Atualizar dinheiro
  dinheiroElemento.innerHTML = "$<span id='valor-dinheiro'>" + dinheiro + "</span>";

  // Atualizar vida
  vidaElemento.innerHTML = "<span id='valor-vida'>" + vida + "</span>";

  // Definir cor da vida com base no valor
  if (vida <= 20) {
    vidaElemento.style.color = "#ff0000";
    vidaElemento.style.boxShadow = "0 0 10px rgba(255, 0, 0, 0.7)";
  } else if (vida <= 50) {
    vidaElemento.style.color = "#ffaa00";
    vidaElemento.style.boxShadow = "0 0 10px rgba(255, 170, 0, 0.7)";
  } else {
    vidaElemento.style.color = "#ffffff";
    vidaElemento.style.boxShadow = "0 0 10px rgba(204, 255, 0, 0.5)";
  }

  // Atualizar munição
  municaoPrimariaElemento.textContent = municaoPrimaria;
  municaoReservaElemento.textContent = "/ " + municaoReserva;

  // Destacar munição baixa
  if (municaoPrimaria <= 5) {
    municaoPrimariaElemento.style.color = "#ff0000";
  } else {
    municaoPrimariaElemento.style.color = "#ffffff";
  }
}

// Atualizar o tempo
function atualizarTempo() {
  if (tempoRestante > 0) {
    tempoRestante--;

    // Converter segundos para formato MM:SS
    const minutos = Math.floor(tempoRestante / 60);
    const segundos = tempoRestante % 60;
    tempoElemento.textContent =
      minutos + ":" + (segundos < 10 ? "0" : "") + segundos;

    // Destacar tempo baixo
    if (tempoRestante <= 10) {
      tempoElemento.style.color = "#ff0000";
    }
  }
}

// Funções para simular ações do jogo
function atirar() {
  if (municaoPrimaria > 0) {
    municaoPrimaria--;
    atualizarHUD();
    return true;
  }
  return false;
}

function recarregar() {
  if (municaoReserva > 0 && municaoPrimaria < 30) {
    const municaoNecessaria = 30 - municaoPrimaria;
    const municaoDisponivel = Math.min(municaoNecessaria, municaoReserva);

    municaoPrimaria += municaoDisponivel;
    municaoReserva -= municaoDisponivel;
    atualizarHUD();
    return true;
  }
  return false;
}

function tomarDano(quantidade) {
  vida = Math.max(0, vida - quantidade);
  atualizarHUD();

  if (vida <= 0) {
    // Game over ou respawn
    setTimeout(() => {
      vida = 100;
      atualizarHUD();
    }, 3000);
  }
  return true;
}

// Controle do painel de instruções
function configurarPainelInstrucoes() {
  const painelInstrucoes = document.getElementById("painel-instrucoes");
  const fecharInstrucoes = document.getElementById("fechar-instrucoes");
  const mostrarInstrucoesBotao = document.getElementById("mostrar-instrucoes");

  // Verificar se os elementos existem
  if (!painelInstrucoes || !fecharInstrucoes || !mostrarInstrucoesBotao) {
    console.error("Elementos do painel de instruções não encontrados");
    return;
  }

  // Função para esconder o painel
  function esconderPainel() {
    painelInstrucoes.style.display = "none";
    mostrarInstrucoesBotao.style.display = "flex";

    // Salvar preferência do usuário
    localStorage.setItem("instrucoes-fechadas", "true");
  }

  // Função para mostrar o painel
  function mostrarPainelInstrucoes() {
    painelInstrucoes.style.display = "block";
    mostrarInstrucoesBotao.style.display = "none";

    // Salvar preferência do usuário
    localStorage.setItem("instrucoes-fechadas", "false");
  }

  // Evento para o botão fechar
  fecharInstrucoes.addEventListener("click", esconderPainel);

  // Evento para o botão mostrar
  mostrarInstrucoesBotao.addEventListener("click", mostrarPainelInstrucoes);

  // Verificar preferência salva ou configuração do backend
  const instrucoesFechadas = localStorage.getItem("instrucoes-fechadas") === "true";

  if (!mostrarInstrucoes || instrucoesFechadas) {
    esconderPainel();
  } else {
    mostrarPainelInstrucoes();
  }

  // Piscar o painel de instruções no início para chamar atenção
  if (mostrarInstrucoes && !instrucoesFechadas) {
    setTimeout(() => {
      if (painelInstrucoes.style.display !== "none") {
        painelInstrucoes.style.animation = "pulsar 2s infinite";

        // Parar de piscar após 5 segundos
        setTimeout(() => {
          painelInstrucoes.style.animation = "none";
        }, 5000);
      }
    }, 3000);
  }
}

// Adicionar eventos para teclado e mouse
function adicionarEventosTeste() {
  // Tecla R para recarregar
  document.addEventListener("keydown", (evento) => {
    if (evento.key.toLowerCase() === "r") {
      recarregar();
    }
  });

  // Clique para atirar (excluindo cliques no avatar e interface)
  document.addEventListener("click", (evento) => {
    // Verificar se o clique foi no avatar, no painel de instruções ou na entrada
    const containerAvatar = document.getElementById("container-avatar");
    const painelInstrucoes = document.getElementById("painel-instrucoes");
    const entradaUsuario = document.getElementById("entrada-usuario");
    const mostrarInstrucoes = document.getElementById("mostrar-instrucoes");

    // Evitar atirar quando clicar em elementos interativos
    if (
      !containerAvatar.contains(evento.target) &&
      !painelInstrucoes.contains(evento.target) &&
      evento.target !== entradaUsuario &&
      evento.target !== mostrarInstrucoes &&
      !evento.target.closest(".balao-fala") &&
      !evento.target.closest(".area-entrada")
    ) {
      atirar();
    }
  });

  // Tecla D para tomar dano (apenas para teste)
  document.addEventListener("keydown", (evento) => {
    if (evento.key.toLowerCase() === "d") {
      tomarDano(10);
    }
  });
}

// Inicializar quando a página carregar
document.addEventListener("DOMContentLoaded", () => {
  inicializarHUD();
  configurarPainelInstrucoes();
  
  // Adicionar eventos de interação após um pequeno delay
  setTimeout(() => {
    adicionarEventosTeste();
  }, 1000);
});

// Disponibilizar funções para outros scripts
window.atirar = atirar;
window.recarregar = recarregar;
window.tomarDano = tomarDano;