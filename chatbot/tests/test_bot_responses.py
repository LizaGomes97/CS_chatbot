"""
Teste automatizado para as respostas do chatbot
Salve este arquivo como chatbot/tests/test_bot_responses.py
Execute com: python manage.py test chatbot.tests
"""

from django.test import TestCase
from chatbot.models import BotResponse, ResponseCategory, Emotion
from chatbot.views import get_bot_response, format_response

class BotResponseTests(TestCase):
    """Testes automatizados para o sistema de respostas do chatbot"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar categorias de teste
        self.cat_generic = ResponseCategory.objects.create(
            name="Genérico", 
            description="Respostas genéricas"
        )
        self.cat_weapons = ResponseCategory.objects.create(
            name="Armas", 
            description="Informações sobre armas"
        )
        self.cat_maps = ResponseCategory.objects.create(
            name="Mapas", 
            description="Informações sobre mapas"
        )
        
        # Criar uma emoção de teste
        self.emotion = Emotion.objects.create(
            name="Teste",
            animation_name="Idle",
            expression_name=None,
            expression_intensity=0.0
        )
        
        # Criar respostas de teste
        self.generic_response = BotResponse.objects.create(
            category=self.cat_generic,
            trigger_keywords="ajuda, help",
            response_text="Como posso ajudar?",
            emotion=self.emotion,
            is_active=True,
            priority=5
        )
        
        self.armas_response = BotResponse.objects.create(
            category=self.cat_weapons,
            trigger_keywords="armas, Armas, weapons",
            response_text="Sobre qual arma você quer falar? Sniper, ak-47, m4...",
            emotion=self.emotion,
            is_active=True,
            priority=5
        )
        
        self.ak47_response = BotResponse.objects.create(
            category=self.cat_weapons,
            trigger_keywords="ak, ak-47, ak47",
            response_text="A AK-47 é a arma principal dos terroristas.",
            emotion=self.emotion,
            is_active=True,
            priority=10
        )
        
        self.maps_response = BotResponse.objects.create(
            category=self.cat_maps,
            trigger_keywords="mapas, Mapas, maps",
            response_text="Sobre qual mapa você quer falar? Mirage ou Dust2?",
            emotion=self.emotion,
            is_active=True,
            priority=5
        )
    
    def test_keywords_list_method(self):
        """Testa se o método keywords_list está funcionando corretamente"""
        # Testa cada resposta criada
        for response in [self.generic_response, self.armas_response, self.ak47_response, self.maps_response]:
            print(f"Testando keywords_list para resposta {response.id}")
            print(f"  trigger_keywords: '{response.trigger_keywords}'")
            keywords = response.keywords_list
            print(f"  keywords_list: {keywords}")
            
            # Verifica se as palavras-chave foram corretamente separadas
            self.assertIsInstance(keywords, list, "keywords_list deve retornar uma lista")
            self.assertEqual(len(keywords), len(response.trigger_keywords.split(',')), 
                            f"Número incorreto de palavras-chave para '{response.trigger_keywords}'")
            
            # Verifica cada palavra-chave individualmente
            for kw in response.trigger_keywords.split(','):
                expected_kw = kw.strip().lower()
                self.assertIn(expected_kw, keywords, 
                             f"Palavra-chave '{expected_kw}' não encontrada na lista {keywords}")
    
    def test_get_bot_response_exact_match(self):
        """Testa se a função get_bot_response encontra correspondências exatas"""
        test_cases = [
            ("ajuda", "Como posso ajudar?"),
            ("help", "Como posso ajudar?"),
            ("armas", "Sobre qual arma você quer falar? Sniper, ak-47, m4..."),
            ("Armas", "Sobre qual arma você quer falar? Sniper, ak-47, m4..."),
            ("weapons", "Sobre qual arma você quer falar? Sniper, ak-47, m4..."),
            ("ak-47", "A AK-47 é a arma principal dos terroristas."),
            ("ak47", "A AK-47 é a arma principal dos terroristas."),
            ("mapas", "Sobre qual mapa você quer falar? Mirage ou Dust2?"),
        ]
        
        for input_text, expected_output in test_cases:
            print(f"\nTestando correspondência exata para input: '{input_text}'")
            response = get_bot_response(input_text)
            print(f"Resposta obtida: {response}")
            self.assertIn('text', response, f"Resposta para '{input_text}' não contém campo 'text'")
            self.assertEqual(response['text'], expected_output, 
                            f"Resposta incorreta para '{input_text}'. Esperado: '{expected_output}', Obtido: '{response['text']}'")
    
    def test_get_bot_response_with_context(self):
        """Testa se a função get_bot_response encontra correspondências em contexto"""
        test_cases = [
            ("Quero saber sobre armas", "Sobre qual arma você quer falar? Sniper, ak-47, m4..."),
            ("Me fale sobre a AK-47", "A AK-47 é a arma principal dos terroristas."),
            ("Quais mapas existem?", "Sobre qual mapa você quer falar? Mirage ou Dust2?"),
        ]
        
        for input_text, expected_output in test_cases:
            print(f"\nTestando correspondência em contexto para input: '{input_text}'")
            response = get_bot_response(input_text)
            print(f"Resposta obtida: {response}")
            self.assertIn('text', response, f"Resposta para '{input_text}' não contém campo 'text'")
            self.assertEqual(response['text'], expected_output, 
                            f"Resposta incorreta para '{input_text}'. Esperado: '{expected_output}', Obtido: '{response['text']}'")
    
    def test_format_response(self):
        """Testa se a função format_response formata corretamente a resposta"""
        response = format_response(self.armas_response)
        print(f"Resposta formatada: {response}")
        
        # Verifica campos obrigatórios
        self.assertIn('text', response)
        self.assertIn('animation', response)
        self.assertIn('expression', response)
        self.assertIn('expression_intensity', response)
        
        # Verifica valores específicos
        self.assertEqual(response['text'], self.armas_response.response_text)
        self.assertEqual(response['animation'], "Idle")  # Valor padrão de teste
    
    def test_response_fallback(self):
        """Testa se a resposta genérica é retornada quando não há correspondência"""
        # Criar uma mensagem que não corresponde a nenhuma palavra-chave
        input_text = "texto completamente aleatório sem correspondência"
        
        print(f"\nTestando fallback para input: '{input_text}'")
        response = get_bot_response(input_text)
        print(f"Resposta obtida: {response}")
        
        # Verifica se a resposta fallback foi retornada
        self.assertIn('text', response)
        # Verifica se é a resposta padrão quando não há correspondência
        self.assertIn("Não entendi bem", response['text'], "Resposta fallback incorreta")
    
    def test_response_priority(self):
        """Testa se a prioridade das respostas é respeitada"""
        # Criar outra resposta para a mesma palavra-chave, mas com prioridade maior
        high_priority_response = BotResponse.objects.create(
            category=self.cat_weapons,
            trigger_keywords="armas",
            response_text="Resposta de alta prioridade",
            emotion=self.emotion,
            is_active=True,
            priority=20  # Prioridade maior
        )
        
        # Testar se a resposta de maior prioridade é retornada
        input_text = "armas"
        print(f"\nTestando prioridade para input: '{input_text}'")
        response = get_bot_response(input_text)
        print(f"Resposta obtida: {response}")
        
        self.assertEqual(response['text'], "Resposta de alta prioridade", 
                        "A resposta de maior prioridade não foi retornada")
    
    def test_debug_responses(self):
        """Teste especial para depurar todas as respostas no banco de dados"""
        print("\n==== DEPURAÇÃO DE TODAS AS RESPOSTAS NO BANCO ====")
        all_responses = BotResponse.objects.filter(is_active=True)
        print(f"Total de respostas ativas: {all_responses.count()}")
        
        for response in all_responses:
            print(f"\nID: {response.id}")
            print(f"Categoria: {response.category.name}")
            print(f"trigger_keywords: '{response.trigger_keywords}'")
            try:
                keywords_list = response.keywords_list
                print(f"keywords_list: {keywords_list}")
            except Exception as e:
                print(f"ERRO ao acessar keywords_list: {e}")
            print(f"Texto: {response.response_text[:100]}...")
            print(f"Prioridade: {response.priority}")
            print(f"Ativo: {response.is_active}")