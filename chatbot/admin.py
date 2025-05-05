from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

from .models import (
    Avatar, 
    Emotion, 
    ResponseCategory, 
    BotResponse, 
    HUDSetting,
    GameCommand,
    ChatSession,
    ChatMessage
)

@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_url', 'is_default', 'date_added')
    list_filter = ('is_default', 'date_added')
    search_fields = ('name', 'model_url')
    actions = ['make_default']
    
    def make_default(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, _("Apenas um avatar pode ser definido como padrão por vez."), level='error')
            return
        
        queryset.update(is_default=True)
        self.message_user(request, _("Avatar definido como padrão."))
    make_default.short_description = _("Definir como avatar padrão")


@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'animation_name', 'expression_name', 'expression_intensity', 'response_count')
    search_fields = ('name', 'animation_name', 'expression_name')
    list_filter = ('animation_name', 'expression_name')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            response_count=Count('responses', distinct=True),
        )
        return queryset
    
    def response_count(self, obj):
        return obj.response_count
    response_count.short_description = _("Nº de Respostas")
    response_count.admin_order_field = 'response_count'


class BotResponseInline(admin.TabularInline):
    model = BotResponse
    extra = 1
    fields = ('response_text', 'trigger_keywords', 'emotion', 'priority', 'is_active')


@admin.register(ResponseCategory)
class ResponseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'response_count')
    search_fields = ('name', 'description')
    inlines = [BotResponseInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(response_count=Count('responses'))
        return queryset
    
    def response_count(self, obj):
        return obj.response_count
    response_count.short_description = _("Nº de Respostas")
    response_count.admin_order_field = 'response_count'


@admin.register(BotResponse)
class BotResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'short_response', 'emotion', 'priority', 'is_active', 'updated_at')
    list_filter = ('category', 'emotion', 'is_active', 'created_at', 'updated_at')
    search_fields = ('response_text', 'trigger_keywords')
    list_editable = ('priority', 'is_active')
    autocomplete_fields = ['category', 'emotion']
    fieldsets = (
        (None, {
            'fields': ('category', 'response_text', 'is_active')
        }),
        (_("Configurações de Reconhecimento"), {
            'fields': ('trigger_keywords', 'priority'),
            'description': _("Configure como esta resposta é acionada e sua prioridade em relação a outras.")
        }),
        (_("Configurações de Exibição"), {
            'fields': ('emotion',),
            'description': _("Configure como a resposta será visualizada no chatbot.")
        }),
    )
    
    def short_response(self, obj):
        if len(obj.response_text) > 50:
            return f"{obj.response_text[:50]}..."
        return obj.response_text
    short_response.short_description = _("Resposta")


@admin.register(HUDSetting)
class HUDSettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'initial_money', 'initial_health', 'initial_ammo_primary', 
                   'initial_ammo_reserve', 'round_time_seconds', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    actions = ['make_active']
    
    def make_active(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, _("Apenas uma configuração pode ser ativada por vez."), level='error')
            return
        
        queryset.update(is_active=True)
        self.message_user(request, _("Configuração HUD ativada com sucesso."))
    make_active.short_description = _("Ativar configuração de HUD")


@admin.register(GameCommand)
class GameCommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'command_type', 'short_keywords', 'emotion', 'is_active')
    list_filter = ('command_type', 'is_active')
    search_fields = ('name', 'trigger_keywords', 'response_text')
    list_editable = ('is_active',)
    
    def short_keywords(self, obj):
        if len(obj.trigger_keywords) > 50:
            return f"{obj.trigger_keywords[:50]}..."
        return obj.trigger_keywords
    short_keywords.short_description = _("Palavras-chave")


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('is_user', 'message', 'timestamp', 'response')
    fields = ('timestamp', 'is_user', 'message', 'response')
    can_delete = False
    max_num = 0
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user_name', 'start_time', 'end_time', 'is_active', 'message_count')
    list_filter = ('is_active', 'start_time', 'end_time')
    search_fields = ('session_id', 'user_name')
    readonly_fields = ('session_id', 'start_time', 'message_count')
    inlines = [ChatMessageInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(message_count=Count('messages'))
        return queryset
    
    def message_count(self, obj):
        return obj.message_count
    message_count.short_description = _("Nº de Mensagens")
    message_count.admin_order_field = 'message_count'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_link', 'is_user', 'short_message', 'timestamp')
    list_filter = ('is_user', 'timestamp', 'session')
    search_fields = ('message', 'session__user_name', 'session__session_id')
    readonly_fields = ('session', 'is_user', 'message', 'timestamp', 'response')
    
    def has_add_permission(self, request):
        return False
    
    def short_message(self, obj):
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    short_message.short_description = _("Mensagem")
    
    def session_link(self, obj):
        url = reverse('admin:chatbot_chatsession_change', args=[obj.session.id])
        return format_html('<a href="{}">{}</a>', url, obj.session)
    session_link.short_description = _("Sessão")
    session_link.admin_order_field = 'session'


# Personalizar o Admin Site
admin.site.site_header = _("Administração do Chatbot CS")
admin.site.site_title = _("Painel de Controle do Chatbot")
admin.site.index_title = _("Bem-vindo ao Painel de Administração do CS Chatbot")