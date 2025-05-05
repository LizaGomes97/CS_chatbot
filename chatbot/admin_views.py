from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.db.models import Count, Sum, Q, Case, When, Value, IntegerField
from django.utils import timezone
from datetime import timedelta

from .models import ChatSession, ChatMessage, BotResponse, Avatar, Emotion, HUDSetting

@staff_member_required
def admin_dashboard(request):
    """Vista personalizada para o dashboard administrativo"""
    
    # Estatísticas gerais
    total_sessions = ChatSession.objects.count()
    active_sessions = ChatSession.objects.filter(is_active=True).count()
    total_messages = ChatMessage.objects.count()
    
    # Usuários únicos (baseados em nomes de usuário não nulos e distintos)
    unique_users = ChatSession.objects.exclude(user_name__isnull=True).values('user_name').distinct().count()
    
    # Estatísticas de respostas
    total_responses = BotResponse.objects.count()
    active_responses = BotResponse.objects.filter(is_active=True).count()
    
    # Respostas mais utilizadas
    top_responses = ChatMessage.objects.filter(
        is_user=False, 
        response__isnull=False
    ).values(
        'response__response_text', 
        'response__category__name'
    ).annotate(
        usage_count=Count('id')
    ).order_by('-usage_count')[:5]
    
    # Categorias de resposta mais comuns
    top_categories = BotResponse.objects.values(
        'category__name'
    ).annotate(
        response_count=Count('id')
    ).order_by('-response_count')[:5]
    
    # Atividade recente - sessões das últimas 24 horas
    recent_timeframe = timezone.now() - timedelta(hours=24)
    recent_sessions = ChatSession.objects.filter(
        start_time__gte=recent_timeframe
    ).count()
    
    recent_messages = ChatMessage.objects.filter(
        timestamp__gte=recent_timeframe
    ).count()
    
    # Gráfico de atividade por hora (últimas 24 horas)
    hourly_activity = []
    for hour in range(24):
        hour_start = timezone.now() - timedelta(hours=24-hour)
        hour_end = timezone.now() - timedelta(hours=23-hour)
        
        message_count = ChatMessage.objects.filter(
            timestamp__gte=hour_start,
            timestamp__lt=hour_end
        ).count()
        
        hourly_activity.append({
            'hour': hour_start.strftime('%H:%M'),
            'count': message_count
        })
    
    # Contagem de tipos de mensagens (usuário vs bot)
    message_types = ChatMessage.objects.aggregate(
        user_messages=Count(Case(When(is_user=True, then=1))),
        bot_messages=Count(Case(When(is_user=False, then=1)))
    )
    
    # Contexto para o template
    context = {
        'title': 'Dashboard do CS Chatbot',
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
        'total_messages': total_messages,
        'unique_users': unique_users,
        'total_responses': total_responses,
        'active_responses': active_responses,
        'top_responses': top_responses,
        'top_categories': top_categories,
        'recent_sessions': recent_sessions,
        'recent_messages': recent_messages,
        'hourly_activity': hourly_activity,
        'message_types': message_types,
        # Contagens adicionais para o template index.html
        'sessions_count': total_sessions,
        'responses_count': total_responses,
        'users_count': unique_users,
    }
    
    return TemplateResponse(request, 'admin/dashboard.html', context)