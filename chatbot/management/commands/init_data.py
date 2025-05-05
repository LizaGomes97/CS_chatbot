from django.core.management.base import BaseCommand
from chatbot.models import Avatar, Emotion, ResponseCategory, BotResponse, GameCommand, HUDSetting
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = 'Inicializa os dados básicos do chatbot'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando a criação de dados iniciais...')
        
        # Criar avatar padrão
        self.create_default_avatar()
        
        # Criar emoções padrão
        self.create_default_emotions()
        
        # Criar categorias de resposta
        self.create_response_categories()
        
        # Criar respostas padrão
        self.create_default_responses()
        
        # Criar configurações de HUD
        self.create_hud_settings()
        
        # Criar comandos de jogo
        self.create_game_commands()
        
        self.stdout.write(self.style.SUCCESS('Dados iniciais criados com sucesso!'))
    
    def create_default_avatar(self):
        """Cria o avatar padrão do robô"""
        self.stdout.write('Criando avatar padrão...')
        
        Avatar.objects.get_or_create(
            name='Robô CS',
            defaults={
                'model_url': 'https://threejs.org/examples/models/gltf/RobotExpressive/RobotExpressive.glb',
                'is_default': True
            }
        )
    
    def create_default_emotions(self):
        """Cria as emoções padrão do robô"""
        self.stdout.write('Criando emoções padrão...')
        
        emotions_data = [
            {
                'name': 'Neutro',
                'animation_name': 'Idle',
                'expression_name': None,
                'expression_intensity': 0
            },
            {
                'name': 'Feliz',
                'animation_name': 'Jump',
                'expression_name': 'Happy',
                'expression_intensity': 1.0
            },
            {
                'name': 'Triste',
                'animation_name': 'Idle',
                'expression_name': 'Sad',
                'expression_intensity': 1.0
            },
            {
                'name': 'Surpreso',
                'animation_name': 'Jump',
                'expression_name': 'Surprised',
                'expression_intensity': 1.0
            },
            {
                'name': 'Animado',
                'animation_name': 'Dance',
                'expression_name': 'Happy',
                'expression_intensity': 1.0
            },
            {
                'name': 'Explicativo',
                'animation_name': 'Wave',
                'expression_name': None,
                'expression_intensity': 0
            },
            {
                'name': 'Aprovação',
                'animation_name': 'ThumbsUp',
                'expression_name': 'Happy',
                'expression_intensity': 0.7
            },
            {
                'name': 'Combativo',
                'animation_name': 'Punch',
                'expression_name': None,
                'expression_intensity': 0
            },
            {
                'name': 'Positivo',
                'animation_name': 'Yes',
                'expression_name': 'Happy',
                'expression_intensity': 0.5
            },
            {
                'name': 'Negativo',
                'animation_name': 'No',
                'expression_name': 'Sad',
                'expression_intensity': 0.5
            },
        ]
        
        for emotion_data in emotions_data:
            Emotion.objects.get_or_create(
                name=emotion_data['name'],
                defaults={
                    'animation_name': emotion_data['animation_name'],
                    'expression_name': emotion_data['expression_name'],
                    'expression_intensity': emotion_data['expression_intensity']
                }
            )
    
    def create_response_categories(self):
        """Cria categorias para as respostas do bot"""
        self.stdout.write('Criando categorias de resposta...')
        
        categories_data = [
            {
                'name': 'Genérico',
                'description': 'Respostas genéricas para quando não há correspondência específica'
            },
            {
                'name': 'Armas',
                'description': 'Informações sobre armas do jogo'
            },
            {
                'name': 'Mapas',
                'description': 'Informações sobre mapas do jogo'
            },
            {
                'name': 'Táticas',
                'description': 'Dicas táticas e estratégias'
            },
            {
                'name': 'Saudações',
                'description': 'Saudações e mensagens de boas-vindas'
            },
            {
                'name': 'Economia',
                'description': 'Dicas sobre gerenciamento de dinheiro no jogo'
            },
            {
                'name': 'Acessórios',
                'description': 'Informações sobre granadas, kits de defesa e outros itens'
            },
        ]
        
        for category_data in categories_data:
            ResponseCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description']
                }
            )
    
    def create_default_responses(self):
        """Cria respostas padrão para o bot"""
        self.stdout.write('Criando respostas padrão...')
        
        # Obter categorias
        try:
            generic_category = ResponseCategory.objects.get(name='Genérico')
            weapons_category = ResponseCategory.objects.get(name='Armas')
            maps_category = ResponseCategory.objects.get(name='Mapas')
            tactics_category = ResponseCategory.objects.get(name='Táticas')
            greetings_category = ResponseCategory.objects.get(name='Saudações')
            economy_category = ResponseCategory.objects.get(name='Economia')
            accessories_category = ResponseCategory.objects.get(name='Acessórios')
            
            # Obter emoções
            neutral_emotion = Emotion.objects.get(name='Neutro')
            happy_emotion = Emotion.objects.get(name='Feliz')
            explaining_emotion = Emotion.objects.get(name='Explicativo')
            approval_emotion = Emotion.objects.get(name='Aprovação')
            positive_emotion = Emotion.objects.get(name='Positivo')
            combat_emotion = Emotion.objects.get(name='Combativo')
            
            # Criar respostas genéricas
            BotResponse.objects.get_or_create(
                category=generic_category,
                trigger_keywords='ajuda, ajudar, help',
                defaults={
                    'response_text': 'Posso te ajudar com informações sobre armas, mapas, táticas e economia do Counter-Strike. O que você gostaria de saber?',
                    'emotion': explaining_emotion,
                    'priority': 5
                }
            )
            
            BotResponse.objects.get_or_create(
                category=generic_category,
                trigger_keywords='oi, olá, ola, hey, hello',
                defaults={
                    'response_text': 'Olá! Estou aqui para falar sobre Counter-Strike. Como posso ajudar hoje?',
                    'emotion': happy_emotion,
                    'priority': 5
                }
            )
            
            # Respostas sobre armas
            BotResponse.objects.get_or_create(
                category=weapons_category,
                trigger_keywords='awp, sniper',
                defaults={
                    'response_text': 'A AWP é a arma mais poderosa do jogo! Um tiro em qualquer parte do corpo (exceto pernas) é fatal. Custa 4750$ e tem recarga lenta, mas vale a pena para quem tem boa mira.',
                    'emotion': approval_emotion,
                    'priority': 10
                }
            )
            
            BotResponse.objects.get_or_create(
                category=weapons_category,
                trigger_keywords='ak, ak-47, ak47',
                defaults={
                    'response_text': 'A AK-47 é a arma principal dos terroristas. Tem alta precisão no primeiro tiro e mata com um headshot mesmo com capacete. Dominar o spray dela é essencial para ser competitivo!',
                    'emotion': positive_emotion,
                    'priority': 10
                }
            )
            
            BotResponse.objects.get_or_create(
                category=weapons_category,
                trigger_keywords='m4, m4a4, m4a1, m4a1-s',
                defaults={
                    'response_text': 'A M4A4 e M4A1-S são as principais armas dos CTs. A M4A4 tem mais balas (30) e cadência maior, enquanto a M4A1-S é silenciada e tem melhor precisão com 20 balas.',
                    'emotion': explaining_emotion,
                    'priority': 10
                }
            )
            
            # Respostas sobre mapas
            BotResponse.objects.get_or_create(
                category=maps_category,
                trigger_keywords='dust, dust2, d2',
                defaults={
                    'response_text': 'Dust2 é o mapa mais icônico de CS! Tem layout simples e equilibrado para os dois lados. A tática "Rush B" foi imortalizada neste mapa.',
                    'emotion': positive_emotion,
                    'priority': 10
                }
            )
            
            BotResponse.objects.get_or_create(
                category=maps_category,
                trigger_keywords='mirage',
                defaults={
                    'response_text': 'Mirage é um mapa muito jogado em competições. Tem um layout médio com três entradas para o bombsite A e duas para o B. Os "smokes" no meio e bombsite A são essenciais.',
                    'emotion': explaining_emotion,
                    'priority': 10
                }
            )
            
            # Respostas sobre táticas
            BotResponse.objects.get_or_create(
                category=tactics_category,
                trigger_keywords='rush, rushar, rushando',
                defaults={
                    'response_text': 'Rush é uma tática onde todo o time avança rapidamente para um bombsite. Funciona melhor quando o inimigo não espera! Rush B no Dust2 é um clássico.',
                    'emotion': combat_emotion,
                    'priority': 8
                }
            )
            
            BotResponse.objects.get_or_create(
                category=tactics_category,
                trigger_keywords='smoke, fumaça, granada de fumaça',
                defaults={
                    'response_text': 'Granadas de fumaça são essenciais para bloquear linhas de visão do inimigo. Aprender os pontos corretos para lançá-las em cada mapa é fundamental para jogadas táticas.',
                    'emotion': explaining_emotion,
                    'priority': 8
                }
            )
            
            # Respostas sobre economia
            BotResponse.objects.get_or_create(
                category=economy_category,
                trigger_keywords='eco, economia, economizar',
                defaults={
                    'response_text': 'Rounds de eco são quando o time economiza dinheiro, comprando pouco ou nada. É uma estratégia importante quando seu time está com pouco dinheiro, para garantir um full buy no próximo round.',
                    'emotion': explaining_emotion,
                    'priority': 7
                }
            )
            
            BotResponse.objects.get_or_create(
                category=economy_category,
                trigger_keywords='force, force buy, forçar',
                defaults={
                    'response_text': 'Force buy é quando o time compra armas mesmo sem dinheiro suficiente para equipamento completo. Útil quando o placar está desfavorável e não dá para esperar.',
                    'emotion': explaining_emotion,
                    'priority': 7
                }
            )
            
        except ResponseCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('Erro: Categorias não encontradas. Verifique se foram criadas corretamente.'))
        except Emotion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Erro: Emoções não encontradas. Verifique se foram criadas corretamente.'))
    
    def create_hud_settings(self):
        """Cria configurações padrão para o HUD"""
        self.stdout.write('Criando configurações de HUD...')
        
        HUDSetting.objects.get_or_create(
            name='Padrão',
            defaults={
                'initial_money': 7000,
                'initial_health': 100,
                'initial_ammo_primary': 30,
                'initial_ammo_reserve': 90,
                'round_time_seconds': 105,
                'show_instructions_panel': True,
                'is_active': True
            }
        )
        
        HUDSetting.objects.get_or_create(
            name='Competitivo',
            defaults={
                'initial_money': 800,
                'initial_health': 100,
                'initial_ammo_primary': 30,
                'initial_ammo_reserve': 90,
                'round_time_seconds': 115,
                'show_instructions_panel': False,
                'is_active': False
            }
        )
    
    def create_game_commands(self):
        """Cria comandos de jogo para o chatbot"""
        self.stdout.write('Criando comandos de jogo...')
        
        try:
            # Obter emoções para os comandos
            combat_emotion = Emotion.objects.get(name='Combativo')
            approval_emotion = Emotion.objects.get(name='Aprovação')
            surprised_emotion = Emotion.objects.get(name='Surpreso')
            
            # Criar comandos
            GameCommand.objects.get_or_create(
                name='Atirar',
                defaults={
                    'command_type': 'action',
                    'trigger_keywords': 'atirar, tiro, disparo, shoot, fire, bang',
                    'response_text': 'Atirando! Controle o recuo da arma para maior precisão.',
                    'emotion': combat_emotion,
                    'is_active': True
                }
            )
            
            GameCommand.objects.get_or_create(
                name='Recarregar',
                defaults={
                    'command_type': 'action',
                    'trigger_keywords': 'recarregar, reload, munição',
                    'response_text': 'Recarregando! Sempre recarregue em locais seguros para não ser pego de surpresa.',
                    'emotion': approval_emotion,
                    'is_active': True
                }
            )
            
            GameCommand.objects.get_or_create(
                name='Tomar Dano',
                defaults={
                    'command_type': 'action',
                    'trigger_keywords': 'dano, damage, ferir, hit, tomar tiro',
                    'response_text': 'Cuidado! Você tomou dano. Procure cobertura e use kit médico se tiver!',
                    'emotion': surprised_emotion,
                    'is_active': True
                }
            )
            
        except Emotion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Erro: Emoções não encontradas. Verifique se foram criadas corretamente.'))