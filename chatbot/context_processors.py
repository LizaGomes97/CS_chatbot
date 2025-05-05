from .models import ChatSession, ChatMessage, BotResponse, Avatar, Emotion, HUDSetting, GameCommand

def admin_stats(request):
    """
    Adiciona estatísticas básicas a todos os templates do admin para uso no dashboard.
    Só executa as consultas quando estamos no admin para evitar impacto de performance
    no site principal.
    """
    if not request.path.startswith('/admin/'):
        return {}
        
    # Só calcular estatísticas se estiver no admin e o usuário for staff
    if not (request.user.is_authenticated and request.user.is_staff):
        return {}
    
    try:
        # Estatísticas básicas
        sessions_count = ChatSession.objects.count()
        responses_count = BotResponse.objects.count()
        users_count = ChatSession.objects.exclude(user_name__isnull=True).values('user_name').distinct().count()
        
        # Calcular percentuais de tipos de mensagem
        message_counts = ChatMessage.objects.count()
        user_messages = ChatMessage.objects.filter(is_user=True).count()
        bot_messages = ChatMessage.objects.filter(is_user=False).count()
        
        # Evitar divisão por zero
        if message_counts > 0:
            user_messages_percentage = int((user_messages / message_counts) * 100)
            bot_messages_percentage = 100 - user_messages_percentage
        else:
            user_messages_percentage = 0
            bot_messages_percentage = 0
            
        return {
            'sessions_count': sessions_count,
            'responses_count': responses_count,
            'users_count': users_count,
            'message_types': {
                'user_messages': user_messages,
                'bot_messages': bot_messages,
                'user_messages_percentage': user_messages_percentage,
                'bot_messages_percentage': bot_messages_percentage,
            }
        }
    except:
        # Em caso de erro (ex: tabelas ainda não existem), retorna vazio
        return {}