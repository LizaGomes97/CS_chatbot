import json
import uuid
import traceback
import logging
import sys
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q

from .models import (
    Avatar, 
    Emotion, 
    BotResponse, 
    HUDSetting,
    GameCommand,
    ChatSession,
    ChatMessage
)

# Configure um logger para depuração
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def index(request):
    """Renderiza a página principal do chatbot"""
    # Obter o avatar padrão ou o primeiro disponível
    avatar = Avatar.objects.filter(is_default=True).first() or Avatar.objects.first()
    
    # Obter as configurações ativas do HUD
    hud_settings = HUDSetting.objects.filter(is_active=True).first() or HUDSetting.objects.create(
        name="Configuração Padrão",
        is_active=True
    )
    
    # Obter todas as emoções disponíveis
    emotions = list(Emotion.objects.values('name', 'animation_name', 'expression_name', 'expression_intensity'))
    
    # Obter comandos de jogo ativos
    game_commands = list(GameCommand.objects.filter(is_active=True).values(
        'name', 'command_type', 'trigger_keywords'
    ))
    
    # Gerar um ID de sessão único se não existir
    if 'chat_session_id' not in request.session:
        request.session['chat_session_id'] = str(uuid.uuid4())
        
    # Criar ou obter a sessão de chat
    session_id = request.session['chat_session_id']
    chat_session, created = ChatSession.objects.get_or_create(
        session_id=session_id,
        defaults={'is_active': True}
    )
    
    # Se a sessão estava inativa, reativá-la
    if not created and not chat_session.is_active:
        chat_session.is_active = True
        chat_session.end_time = None
        chat_session.save()
    
    # Contexto para o template
    context = {
        'avatar': avatar,
        'hud_settings': hud_settings,
        'emotions_json': json.dumps(emotions),
        'game_commands_json': json.dumps(game_commands),
        'chat_session_id': session_id,
    }
    
    return render(request, 'chatbot/index.html', context)


@csrf_exempt
def process_message(request):
    """Processa mensagens do usuário e retorna respostas do bot"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', request.session.get('chat_session_id'))
        user_name = data.get('user_name', '')
        
        if not user_message:
            return JsonResponse({'error': 'Mensagem vazia'}, status=400)
        
        if not session_id:
            return JsonResponse({'error': 'Sessão inválida'}, status=400)
        
        # Obter ou criar sessão
        chat_session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={'is_active': True}
        )
        
        # Salvar nome do usuário se fornecido
        if user_name and not chat_session.user_name:
            chat_session.user_name = user_name
            chat_session.save()
        
        # Salvar mensagem do usuário
        user_chat_msg = ChatMessage.objects.create(
            session=chat_session,
            is_user=True,
            message=user_message
        )
        
        # Processar comandos de jogo
        game_command = process_game_command(user_message)
        if game_command:
            # Salvar mensagem do bot
            bot_message = ChatMessage.objects.create(
                session=chat_session,
                is_user=False,
                message=game_command['response_text']
            )
            
            return JsonResponse({
                'text': game_command['response_text'],
                'animation': game_command['animation'],
                'expression': game_command['expression'],
                'expression_intensity': game_command['expression_intensity'],
                'command_executed': game_command['command_type']
            })
        
        # Processar resposta normal
        bot_response = get_bot_response(user_message)
        
        # Armazenar a resposta antes de retornar (se ela tiver um ID)
        response_obj = None
        if 'response_id' in bot_response:
            try:
                response_obj = BotResponse.objects.get(id=bot_response['response_id'])
            except:
                # Se não encontrar, continua com None
                pass
        
        # Salvar mensagem do bot
        bot_message = ChatMessage.objects.create(
            session=chat_session,
            is_user=False,
            message=bot_response['text'],
            response=response_obj
        )
        
        # Remover response_id antes de enviar ao cliente (opcional)
        if 'response_id' in bot_response:
            del bot_response['response_id']
        
        return JsonResponse(bot_response)
        
    except Exception as e:
        import traceback
        print(f"Erro ao processar mensagem: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)

def process_game_command(message):
    """Verifica se a mensagem contém comandos de jogo e os processa"""
    try:
        message_lower = message.lower()
        logger.debug(f"Verificando comandos para mensagem: '{message_lower}'")
        
        # Obter todos os comandos ativos
        commands = GameCommand.objects.filter(is_active=True)
        logger.debug(f"Total de comandos ativos: {commands.count()}")
        
        # Verificar se a mensagem corresponde a algum comando
        for command in commands:
            logger.debug(f"Verificando comando: '{command.name}', keywords: {command.trigger_keywords}")
            for keyword in command.keywords_list:
                logger.debug(f"Verificando palavra-chave: '{keyword}'")
                if keyword in message_lower:
                    logger.debug(f"Comando encontrado usando keyword: '{keyword}'")
                    # Obter informações da emoção associada
                    emotion = command.emotion
                    animation = "Idle"  # Animação padrão
                    expression = None
                    expression_intensity = 1.0
                    
                    if emotion:
                        logger.debug(f"Emoção do comando: {emotion.name}")
                        animation = emotion.animation_name
                        expression = emotion.expression_name
                        expression_intensity = emotion.expression_intensity
                    else:
                        logger.debug("Comando sem emoção associada")
                    
                    result = {
                        'command_type': command.command_type,
                        'response_text': command.response_text,
                        'animation': animation,
                        'expression': expression,
                        'expression_intensity': expression_intensity
                    }
                    logger.debug(f"Resultado do comando: {result}")
                    return result
        
        logger.debug("Nenhum comando encontrado")
        return None
    except Exception as e:
        logger.error(f"Erro em process_game_command: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def format_response(response):
    """Formata a resposta do bot com animação e expressão"""
    # Obter informações da emoção associada
    emotion = response.emotion
    animation = "Idle"  # Animação padrão
    expression = None
    expression_intensity = 1.0
    
    if emotion:
        animation = emotion.animation_name
        expression = emotion.expression_name
        expression_intensity = emotion.expression_intensity
    
    # Nota: Não incluir o objeto response diretamente, pois não é serializável para JSON
    result = {
        'text': response.response_text,
        'animation': animation,
        'expression': expression,
        'expression_intensity': expression_intensity,
        'response_id': response.id  # Use ID em vez do objeto completo
    }
    
    return result

def get_bot_response(message):
    """Obtém a resposta mais apropriada do bot com base na mensagem do usuário"""
    try:
        message_lower = message.lower()
        logger.debug(f"Buscando respostas para: '{message_lower}'")
        
        # Buscar todas as respostas ativas
        responses = BotResponse.objects.filter(is_active=True).select_related('emotion', 'category')
        logger.debug(f"Total de respostas ativas: {responses.count()}")
        
        matching_responses = []
        
        # Verificar correspondências de palavras-chave
        for response in responses:
            logger.debug(f"Verificando resposta ID {response.id}, keywords: {response.trigger_keywords}")
            for keyword in response.keywords_list:
                logger.debug(f"Verificando palavra-chave: '{keyword}'")
                if keyword in message_lower:
                    logger.debug(f"Correspondência encontrada com keyword: '{keyword}'")
                    matching_responses.append({
                        'response': response,
                        'priority': response.priority
                    })
                    break
        
        logger.debug(f"Total de correspondências encontradas: {len(matching_responses)}")
        
        # Se não houver correspondências, usar uma resposta genérica
        if not matching_responses:
            logger.debug("Nenhuma correspondência. Buscando resposta genérica.")
            # Buscar respostas da categoria "genérica"
            generic_responses = BotResponse.objects.filter(
                category__name__icontains='genérico',
                is_active=True
            ).select_related('emotion')
            
            logger.debug(f"Respostas genéricas encontradas: {generic_responses.count()}")
            
            if generic_responses.exists():
                # Pegar uma resposta genérica aleatória
                import random
                generic_response = random.choice(generic_responses)
                logger.debug(f"Selecionada resposta genérica ID: {generic_response.id}")
                
                return format_response(generic_response)
            else:
                logger.debug("Nenhuma resposta genérica encontrada. Usando fallback.")
                # Fallback absoluto
                return {
                    'text': "Não entendi bem o que você quis dizer. Pode reformular sua pergunta sobre Counter-Strike?",
                    'animation': "Idle",
                    'expression': None,
                    'expression_intensity': 0
                }
        
        # Ordenar por prioridade (maior primeiro)
        matching_responses.sort(key=lambda x: x['priority'], reverse=True)
        logger.debug(f"Resposta selecionada ID: {matching_responses[0]['response'].id}")
        
        # Pegar a resposta de maior prioridade
        top_response = matching_responses[0]['response']
        
        return format_response(top_response)
    except Exception as e:
        logger.error(f"Erro em get_bot_response: {str(e)}")
        logger.error(traceback.format_exc())
        # Retorna uma resposta de erro, mas não causa falha na API
        return {
            'text': "Desculpe, encontrei um problema ao processar sua mensagem. Tente perguntar de outra forma.",
            'animation': "Sad",
            'expression': "Sad",
            'expression_intensity': 1
        }


@csrf_exempt
def process_message(request):
    """Processa mensagens do usuário e retorna respostas do bot"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', request.session.get('chat_session_id'))
        user_name = data.get('user_name', '')
        
        if not user_message:
            return JsonResponse({'error': 'Mensagem vazia'}, status=400)
        
        if not session_id:
            return JsonResponse({'error': 'Sessão inválida'}, status=400)
        
        # Obter ou criar sessão
        chat_session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={'is_active': True}
        )
        
        # Salvar nome do usuário se fornecido
        if user_name and not chat_session.user_name:
            chat_session.user_name = user_name
            chat_session.save()
        
        # Salvar mensagem do usuário
        user_chat_msg = ChatMessage.objects.create(
            session=chat_session,
            is_user=True,
            message=user_message
        )
        
        # Processar comandos de jogo
        game_command = process_game_command(user_message)
        if game_command:
            # Salvar mensagem do bot
            bot_message = ChatMessage.objects.create(
                session=chat_session,
                is_user=False,
                message=game_command['response_text']
            )
            
            return JsonResponse({
                'text': game_command['response_text'],
                'animation': game_command['animation'],
                'expression': game_command['expression'],
                'expression_intensity': game_command['expression_intensity'],
                'command_executed': game_command['command_type']
            })
        
        # Processar resposta normal
        bot_response = get_bot_response(user_message)
        
        # Armazenar a resposta antes de retornar (se ela tiver um ID)
        response_obj = None
        if 'response_id' in bot_response:
            try:
                response_obj = BotResponse.objects.get(id=bot_response['response_id'])
            except:
                # Se não encontrar, continua com None
                pass
        
        # Salvar mensagem do bot
        bot_message = ChatMessage.objects.create(
            session=chat_session,
            is_user=False,
            message=bot_response['text'],
            response=response_obj
        )
        
        # Remover response_id antes de enviar ao cliente (opcional)
        if 'response_id' in bot_response:
            del bot_response['response_id']
        
        return JsonResponse(bot_response)
        
    except Exception as e:
        import traceback
        print(f"Erro ao processar mensagem: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)

def save_username(request):
    """Salva o nome do usuário na sessão"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        session_id = data.get('session_id', request.session.get('chat_session_id'))
        
        if not username:
            return JsonResponse({'error': 'Nome de usuário inválido'}, status=400)
        
        if not session_id:
            return JsonResponse({'error': 'Sessão inválida'}, status=400)
        
        # Atualizar a sessão
        chat_session = ChatSession.objects.get(session_id=session_id)
        chat_session.user_name = username
        chat_session.save()
        
        return JsonResponse({'success': True, 'username': username})
    
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Sessão não encontrada'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def end_session(request):
    """Finaliza a sessão de chat atual"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        session_id = request.session.get('chat_session_id')
        
        if not session_id:
            return JsonResponse({'error': 'Sessão inválida'}, status=400)
        
        # Atualizar a sessão
        chat_session = ChatSession.objects.get(session_id=session_id)
        chat_session.is_active = False
        chat_session.end_time = timezone.now()
        chat_session.save()
        
        # Limpar o ID da sessão
        del request.session['chat_session_id']
        
        return JsonResponse({'success': True})
    
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Sessão não encontrada'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_hud_settings(request):
    """Retorna as configurações ativas do HUD"""
    hud_settings = HUDSetting.objects.filter(is_active=True).first() or HUDSetting.objects.first()
    
    if not hud_settings:
        return JsonResponse({'error': 'Configurações de HUD não encontradas'}, status=404)
    
    return JsonResponse({
        'initial_money': hud_settings.initial_money,
        'initial_health': hud_settings.initial_health,
        'initial_ammo_primary': hud_settings.initial_ammo_primary,
        'initial_ammo_reserve': hud_settings.initial_ammo_reserve,
        'round_time_seconds': hud_settings.round_time_seconds,
        'show_instructions_panel': hud_settings.show_instructions_panel,
    })