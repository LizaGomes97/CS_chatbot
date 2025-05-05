# CS Chatbot - Django

Um chatbot temático de Counter-Strike desenvolvido com Django, Three.js e tecnologias web modernas. Este projeto permite a criação de um assistente virtual interativo com elementos visuais de HUD do Counter-Strike.

![Screenshot do CS Chatbot](static/images/screenshot.png)

## Características

- **Avatar 3D Interativo**: Personagem 3D animado que reage às interações do usuário
- **Respostas Personalizáveis**: Sistema de administração para gerenciar respostas e comandos
- **Efeitos Visuais de Jogo**: HUD com munição, vida e dinheiro
- **Interação Rica**: O bot responde a cliques, comandos de jogo e perguntas sobre CS
- **Painel Admin Completo**: Interface Django para gerenciar todos os aspectos do chatbot

## Tecnologias Utilizadas

- **Backend**: Django 4.2
- **Frontend**: JavaScript moderno, Three.js
- **3D**: Modelos GLB/GLTF, animações
- **Banco de Dados**: SQLite (padrão), compatível com PostgreSQL/MySQL
- **Interface Admin**: Django Admin personalizado

## Requisitos

- Python 3.8+
- Django 4.2+
- Navegador com suporte a WebGL

## Demonstração Rápida

1. Clone o repositório
2. Configure o ambiente: `python -m venv venv && source venv/bin/activate`
3. Instale dependências: `pip install -r requirements.txt`
4. Aplique migrações: `python manage.py migrate`
5. Crie um superusuário: `python manage.py createsuperuser`
6. Carregue dados iniciais: `python manage.py init_data`
7. Inicie o servidor: `python manage.py runserver`
8. Acesse: `http://localhost:8000/`

## Configuração e Deploy

Para instruções detalhadas de instalação, configuração e uso, consulte o [Guia de Instalação e Uso](INSTALLATION.md).

## Personalização

O sistema é altamente personalizável através do painel de administração Django:

- **Avatares**: Modifique ou substitua o modelo 3D
- **Respostas**: Personalize o que o chatbot diz e como reage
- **Emoções**: Configure expressões faciais e animações
- **HUD**: Ajuste as configurações visuais do HUD
- **Comandos**: Adicione novos comandos de interação

## Telas

### Interface Principal
![Interface Principal](static/images/interface.png)

### Painel Administrativo
![Painel Admin](static/images/admin.png)

## Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir.

## Licença

Este projeto está licenciado sob a MIT License - veja [LICENSE](LICENSE) para detalhes.

## Reconhecimentos

- Three.js pela excelente biblioteca 3D
- Django pela estrutura robusta de backend
- Modelos e texturas de exemplo do Three.js
- Inspiração no jogo Counter-Strike da Valve

## Contato

Para perguntas e sugestões, abra uma issue no GitHub ou entre em contato com [seu-email@exemplo.com].
