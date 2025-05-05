# Guia de Instalação e Uso - Chatbot Counter-Strike em Django

Este guia explica como instalar, configurar e utilizar o Chatbot CS baseado em Django. O sistema permite gerenciar respostas, avatares, expressões e configurações do seu chatbot diretamente pelo admin do Django.

## Requisitos

- Python 3.8+
- Django 4.2+
- Navegador moderno que suporte WebGL (para renderização 3D)

## Instalação

### 1. Clone o repositório

```bash
git clone [URL_DO_REPOSITORIO]
cd cs_chatbot
```

### 2. Configure o ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
# Crie as migrações
python manage.py makemigrations chatbot

# Aplique as migrações
python manage.py migrate
```

### 5. Crie um superusuário para acessar o painel de administração

```bash
python manage.py createsuperuser
```

### 6. Inicialize dados padrão (avatares, emoções, respostas, etc.)

```bash
python manage.py init_data
```

### 7. Colete arquivos estáticos

```bash
python manage.py collectstatic
```

### 8. Inicie o servidor

```bash
python manage.py runserver
```

## Uso do Sistema

### Front-end do Chatbot

O front-end do chatbot estará disponível na URL principal:
```
http://localhost:8000/
```

### Painel Administrativo

Acesse o painel administrativo para gerenciar todos os aspectos do chatbot:
```
http://localhost:8000/admin/
```

Use o nome de usuário e senha criados no passo 5 para fazer login.

## Personalizando o Chatbot

### Avatares

No painel administrativo, vá para "Avatares" para:
- Adicionar novos modelos 3D (URL GLB/GLTF)
- Definir um avatar como padrão
- Remover avatares não utilizados

### Emoções

Em "Emoções", você pode:
- Definir novas emoções associando nomes de animações com expressões faciais
- Controlar a intensidade das expressões (0.0 a 1.0)
- Ver quais respostas usam cada emoção

### Respostas do Bot

Em "Respostas do Bot", você pode:
- Criar novas respostas agrupadas por categorias
- Definir palavras-chave que acionam cada resposta
- Associar emoções a cada resposta
- Definir prioridades (respostas com maior prioridade são escolhidas primeiro em caso de múltiplas correspondências)
- Ativar/desativar respostas

### Comandos de Jogo

Em "Comandos de Jogo", você pode definir ações especiais como:
- Atirar
- Recarregar
- Tomar dano
- Outros comandos personalizados

### Configurações do HUD

Em "Configurações do HUD", você pode personalizar:
- Dinheiro inicial
- Vida inicial
- Munição inicial (primária e reserva)
- Tempo de round
- Visibilidade do painel de instruções

## Monitoramento de Uso

### Sessões de Chat

Em "Sessões de Chat", você pode ver:
- Quais usuários interagiram com o chatbot
- Quando as sessões começaram e terminaram
- Quantas mensagens foram trocadas

### Mensagens de Chat

Em "Mensagens de Chat", você pode analisar:
- Todas as mensagens trocadas com usuários
- Quais respostas foram geradas para cada mensagem
- Horários das interações

## Resolução de Problemas

### Erro no carregamento de modelos 3D

Se o avatar não aparecer:
1. Verifique se a URL do modelo 3D está acessível
2. Confirme que o formato é GLB ou GLTF compatível com Three.js
3. Verifique o console do navegador para erros específicos

### Erro no banco de dados

Se encontrar erros de banco de dados:
```bash
# Remova o banco de dados atual
rm db.sqlite3

# Recrie o banco de dados
python manage.py migrate
python manage.py createsuperuser
python manage.py init_data
```

### Erros de JavaScript

Se encontrar problemas no front-end:
1. Limpe o cache do navegador
2. Verifique o console do navegador para erros específicos
3. Confirme que o navegador suporta as tecnologias necessárias (WebGL, ES6)

## Personalizando o Front-end

Para personalizar a aparência:

1. Edite os arquivos CSS em `static/css/`
2. Modifique os templates em `templates/chatbot/`
3. Atualize os arquivos JavaScript em `static/js/`
4. Execute `python manage.py collectstatic` após alterações

## Contribuindo com o Projeto

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua funcionalidade (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Envie para o GitHub (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request
