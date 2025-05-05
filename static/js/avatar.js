// Importar funções e estados do principal.js
import {
  mudarParaAcao,
  definirExpressao,
  expressoes,
  estados,
  emocoes,
  entradaUsuario,
  chatSessionId,
} from "./principal.js";

// Elementos do DOM
const balaoFala = document.getElementById("balao-fala");
const containerAvatar = document.getElementById("container-avatar");

// Acessar as configurações da aplicação
const apiUrls = window.APP_CONFIG.apiUrls;
const emocoesDoBanco = window.APP_CONFIG.emotions;

// Função para atualizar o balão de fala com efeito de digitação
function atualizarBalaoFala(texto, comDigitacao = true, humor = "neutral") {
  // Definir expressão facial baseada no humor
  switch (humor) {
    case "happy":
      definirExpressao("Happy", 1);
      break;
    case "sad":
      definirExpressao("Sad", 1);
      break;
    case "surprised":
      definirExpressao("Surprised", 1);
      break;
    case "angry":
      definirExpressao("Angry", 1);
      break;
    default:
      // Expressão neutra (reset)
      definirExpressao(null, 0);
  }

  if (comDigitacao) {
    // Adiciona os pontos de "pensando"
    balaoFala.innerHTML =
      '<div class="pontos-pensamento"><span>.</span><span>.</span><span>.</span></div>';

    // Animação "pensando"
    mudarParaAcao("Idle", 0.5);

    // Simula digitação após um breve "pensamento"
    setTimeout(() => {
      balaoFala.textContent = "";
      let i = 0;
      const velocidade = 50; // velocidade de digitação

      function digitador() {
        if (i < texto.length) {
          balaoFala.textContent += texto.charAt(i);
          i++;
          setTimeout(digitador, velocidade);
        } else {
          // Quando terminar de digitar, volta para Idle
          mudarParaAcao("Idle", 0.5);

          // Foca no campo de resposta
          setTimeout(() => {
            entradaUsuario.focus();
          }, 500);
        }
      }

      // Animação "falando"
      mudarParaAcao("Wave", 0.3);

      digitador();
    }, 1000);
  } else {
    balaoFala.textContent = texto;
    // Foca no campo de resposta
    setTimeout(() => {
      entradaUsuario.focus();
    }, 500);
  }
}

// Função para enviar mensagem ao backend e receber a resposta
// Função modificada com debug melhorado
async function enviarMensagem(mensagem) {
  try {
    console.log("Enviando mensagem:", mensagem);
    console.log("Session ID:", chatSessionId);
    
    const body = JSON.stringify({
      message: mensagem,
      session_id: chatSessionId,
    });
    console.log("Corpo da requisição:", body);
    
    const response = await fetch(apiUrls.processMessage, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.APP_CONFIG.csrfToken,
      },
      body: body,
    });

    console.log("Status da resposta:", response.status);
    
    // Clonar a resposta para poder lê-la múltiplas vezes se necessário
    const responseClone = response.clone();
    
    if (!response.ok) {
      let errorMessage = `Erro HTTP ${response.status}`;
      
      try {
        // Tentar ler como JSON primeiro
        const errorData = await response.json();
        console.error("Detalhes do erro HTTP (JSON):", errorData);
        errorMessage += `: ${JSON.stringify(errorData)}`;
      } catch (jsonError) {
        try {
          // Se não for JSON, tenta ler como texto
          const errorText = await responseClone.text();
          console.error("Detalhes do erro HTTP (texto):", errorText);
          errorMessage += `: ${errorText}`;
        } catch (textError) {
          // Se ambos falharem, apenas registrar o status
          console.error("Não foi possível ler o corpo da resposta de erro");
        }
      }
      
      throw new Error(errorMessage);
    }

    // Ler o corpo da resposta como JSON
    const data = await response.json();
    console.log("Resposta recebida:", data);
    return data;
  } catch (error) {
    console.error("Erro ao processar mensagem:", error);
    console.error("Stack trace:", error.stack);
    
    // Mostrar o erro no balão em vez da mensagem genérica (em ambiente de desenvolvimento)
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return {
        text: `Erro técnico: ${error.message}`,
        animation: "Idle", // Usando "Idle" pois "Sad" não está funcionando
        expression: null,  // Usando null pois "Sad" não está funcionando
        expression_intensity: 0,
      };
    } else {
      return {
        text: "Desculpe, tive um problema técnico ao processar sua mensagem. Tente novamente mais tarde.",
        animation: "Idle",
        expression: null,
        expression_intensity: 0,
      };
    }
  }
}

// Função para salvar o nome de usuário no backend
async function salvarNomeUsuario(nome) {
  try {
    const response = await fetch(apiUrls.saveUsername, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.APP_CONFIG.csrfToken,
      },
      body: JSON.stringify({
        username: nome,
        session_id: chatSessionId,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Erro ao salvar nome de usuário:", error);
    return null;
  }
}

// Adicionar interatividade ao avatar
containerAvatar.addEventListener("click", () => {
  const reacoes = [
    {
      texto: "Clicou em mim! Precisa de alguma dica de CS?",
      animacao: "Wave",
      humor: "happy",
    },
    {
      texto: "Oi gamer! Estou aqui para falar sobre Counter-Strike!",
      animacao: "ThumbsUp",
      humor: "happy",
    },
    {
      texto: "Quer saber mais sobre táticas, armas ou mapas?",
      animacao: "Yes",
      humor: "neutral",
    },
    {
      texto: "Pronto para uma partida competitiva?",
      animacao: "Jump",
      humor: "surprised",
    },
    {
      texto: "Rush B, não pare! Haha, clássico de Dust2!",
      animacao: "Punch",
      humor: "happy",
    },
  ];

  const aleatorio = Math.floor(Math.random() * reacoes.length);
  const reacao = reacoes[aleatorio];

  // Definir expressão facial baseada no humor
  definirExpressao(
    reacao.humor === "happy"
      ? "Happy"
      : reacao.humor === "sad"
      ? "Sad"
      : reacao.humor === "surprised"
      ? "Surprised"
      : reacao.humor === "angry"
      ? "Angry"
      : null
  );

  // Executar animação
  mudarParaAcao(reacao.animacao, 0.3);

  // Exibir texto
  atualizarBalaoFala(reacao.texto, true, reacao.humor);
});

// Iniciar o chatbot com uma saudação após carregar a página
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    mudarParaAcao("Wave", 0.3);
    atualizarBalaoFala(
      "Olá jogador! Sou seu assistente virtual de Counter-Strike. Qual seu nickname?",
      true,
      "happy"
    );
  }, 1500);
});

// Exportar funções para uso em outros módulos
export { atualizarBalaoFala, enviarMensagem, salvarNomeUsuario };
