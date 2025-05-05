// Importar funções do avatar.js e principal.js
import { atualizarBalaoFala, enviarMensagem, salvarNomeUsuario } from "./avatar.js";
import { mudarParaAcao, definirExpressao, chatSessionId } from "./principal.js";

// Elementos do DOM
const formularioUsuario = document.getElementById("formulario-usuario");
const entradaUsuario = document.getElementById("entrada-usuario");

// Estado do chat
let nomeUsuario = "";
let conversaIniciada = false;

// Capturar input do usuário
formularioUsuario.addEventListener("submit", async function (e) {
  e.preventDefault();

  const mensagem = entradaUsuario.value.trim();

  if (mensagem) {
    if (!conversaIniciada) {
      // Primeira interação - pegando o nome
      nomeUsuario = mensagem;
      entradaUsuario.value = "";
      
      // Salvar o nome do usuário no backend
      await salvarNomeUsuario(nomeUsuario);

      // Animação de reação do robô
      mudarParaAcao("Jump", 0.3);
      definirExpressao("Happy");

      setTimeout(() => {
        atualizarBalaoFala(
          `Prazer em conhecê-lo, ${nomeUsuario}! Estou aqui para te ajudar a ficar por dentro de tudo sobre CS. Por onde quer começar?`,
          true,
          "happy"
        );
        conversaIniciada = true;
        entradaUsuario.placeholder = "Digite sua pergunta sobre CS...";
        entradaUsuario.focus();
      }, 500);
    } else {
      // Limpar o campo de entrada
      const mensagemEnviada = mensagem;
      entradaUsuario.value = "";
      
      // Processar a mensagem e obter a resposta do backend
      try {
        // Animação "pensando"
        mudarParaAcao("Idle", 0.5);
        
        // Buscar resposta da API
        const resposta = await enviarMensagem(mensagemEnviada);
        
        if (resposta.error) {
          console.error('Erro ao processar mensagem:', resposta.error);
          atualizarBalaoFala(
            `Desculpe, ${nomeUsuario}, tive um problema ao processar sua mensagem. Pode tentar novamente?`,
            true,
            "sad"
          );
          return;
        }
        
        // Executar a animação retornada pelo backend
        if (resposta.animation) {
          mudarParaAcao(resposta.animation, 0.3);
        }
        
        // Definir expressão facial se retornada pelo backend
        if (resposta.expression) {
          definirExpressao(resposta.expression, resposta.expression_intensity || 1);
        }
        
        // Mostrar a resposta com efeito de digitação
        setTimeout(() => {
          atualizarBalaoFala(resposta.text, true);
        }, 500);
        
        // Se houver um comando executado, processar efeitos especiais
        if (resposta.command_executed) {
          processarEfeitosComando(resposta.command_executed);
        }
      } catch (error) {
        console.error('Erro ao processar interação:', error);
        atualizarBalaoFala(
          `Desculpe, ${nomeUsuario}, ocorreu um erro inesperado. Pode tentar novamente mais tarde?`,
          true,
          "sad"
        );
      }
    }
  }
});

// Função para processar efeitos visuais para comandos
function processarEfeitosComando(tipoComando) {
  // Implementar efeitos visuais baseados no tipo de comando
  switch (tipoComando) {
    case 'action':
      // Efeitos para comandos de ação
      break;
    case 'info':
      // Efeitos para comandos de informação
      break;
    case 'setting':
      // Efeitos para comandos de configuração
      break;
    default:
      // Sem efeitos especiais
      break;
  }
}

// Focar no input quando a página carregar
window.addEventListener("load", () => {
  setTimeout(() => {
    entradaUsuario.focus();
  }, 2000);
});

// Exportar variáveis e funções para uso em outros módulos
export { 
  nomeUsuario, 
  conversaIniciada 
};