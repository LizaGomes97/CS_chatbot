from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Avatar(models.Model):
    """Modelo para armazenar informações do avatar 3D"""
    name = models.CharField(_("Nome"), max_length=100)
    model_url = models.URLField(_("URL do modelo 3D"), max_length=500)
    is_default = models.BooleanField(_("Padrão"), default=False)
    date_added = models.DateTimeField(_("Data de adição"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Avatar")
        verbose_name_plural = _("Avatares")
        ordering = ['-is_default', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Se este avatar for definido como padrão, remove o padrão de outros
        if self.is_default:
            Avatar.objects.filter(is_default=True).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)


class Emotion(models.Model):
    """Modelo para mapear emoções a expressões faciais e animações"""
    name = models.CharField(_("Nome"), max_length=50)
    animation_name = models.CharField(_("Nome da animação"), max_length=50)
    expression_name = models.CharField(_("Nome da expressão facial"), max_length=50, blank=True, null=True)
    expression_intensity = models.FloatField(
        _("Intensidade da expressão"), 
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=1.0
    )
    
    class Meta:
        verbose_name = _("Emoção")
        verbose_name_plural = _("Emoções")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ResponseCategory(models.Model):
    """Categoria para respostas (ex: armas, mapas, etc.)"""
    name = models.CharField(_("Nome"), max_length=100)
    description = models.TextField(_("Descrição"), blank=True)
    
    class Meta:
        verbose_name = _("Categoria de Resposta")
        verbose_name_plural = _("Categorias de Resposta")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class BotResponse(models.Model):
    """Modelo para armazenar respostas do bot"""
    category = models.ForeignKey(
        ResponseCategory, 
        on_delete=models.CASCADE, 
        related_name="responses",
        verbose_name=_("Categoria")
    )
    trigger_keywords = models.TextField(_("Palavras-chave de gatilho"))
    response_text = models.TextField(_("Texto da resposta"))
    emotion = models.ForeignKey(
        Emotion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="responses",
        verbose_name=_("Emoção")
    )
    is_active = models.BooleanField(_("Ativo"), default=True)
    priority = models.IntegerField(_("Prioridade"), default=0, help_text=_("Respostas com maior prioridade serão escolhidas primeiro"))
    created_at = models.DateTimeField(_("Criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Atualizado em"), auto_now=True)
    
    class Meta:
        verbose_name = _("Resposta do Bot")
        verbose_name_plural = _("Respostas do Bot")
        ordering = ['-priority', 'category__name']
    
    def __str__(self):
        return f"{self.category.name}: {self.response_text[:50]}..."
    
    @property
    def keywords_list(self):
        """Retorna lista de palavras-chave separadas por vírgula"""
        return [kw.strip().lower() for kw in self.trigger_keywords.split(',') if kw.strip()]


class HUDSetting(models.Model):
    """Configurações visuais do HUD"""
    name = models.CharField(_("Nome da configuração"), max_length=100)
    initial_money = models.IntegerField(_("Dinheiro inicial"), default=7000)
    initial_health = models.IntegerField(_("Vida inicial"), default=100)
    initial_ammo_primary = models.IntegerField(_("Munição primária inicial"), default=30)
    initial_ammo_reserve = models.IntegerField(_("Munição reserva inicial"), default=90)
    round_time_seconds = models.IntegerField(_("Tempo de round (segundos)"), default=105)
    show_instructions_panel = models.BooleanField(_("Mostrar painel de instruções"), default=True)
    is_active = models.BooleanField(_("Ativo"), default=True)
    
    class Meta:
        verbose_name = _("Configuração do HUD")
        verbose_name_plural = _("Configurações do HUD")
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Se esta configuração for ativada, desativa as outras
        if self.is_active:
            HUDSetting.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


class GameCommand(models.Model):
    """Comandos de jogo reconhecidos pelo chatbot"""
    name = models.CharField(_("Nome do comando"), max_length=50)
    command_type = models.CharField(_("Tipo de comando"), max_length=50, choices=[
        ('action', _('Ação')),
        ('info', _('Informação')),
        ('setting', _('Configuração'))
    ])
    trigger_keywords = models.TextField(_("Palavras-chave de gatilho"))
    response_text = models.TextField(_("Texto de resposta ao comando"))
    emotion = models.ForeignKey(
        Emotion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="commands",
        verbose_name=_("Emoção")
    )
    is_active = models.BooleanField(_("Ativo"), default=True)
    
    class Meta:
        verbose_name = _("Comando de Jogo")
        verbose_name_plural = _("Comandos de Jogo")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def keywords_list(self):
        """Retorna lista de palavras-chave separadas por vírgula"""
        return [kw.strip().lower() for kw in self.trigger_keywords.split(',') if kw.strip()]


class ChatSession(models.Model):
    """Armazena informações sobre uma sessão de chat com o usuário"""
    session_id = models.CharField(_("ID de Sessão"), max_length=100, unique=True)
    user_name = models.CharField(_("Nome do usuário"), max_length=100, blank=True, null=True)
    start_time = models.DateTimeField(_("Hora de início"), auto_now_add=True)
    end_time = models.DateTimeField(_("Hora de término"), blank=True, null=True)
    is_active = models.BooleanField(_("Ativo"), default=True)
    
    class Meta:
        verbose_name = _("Sessão de Chat")
        verbose_name_plural = _("Sessões de Chat")
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Sessão {self.session_id[:8]} - {self.user_name or 'Anônimo'}"


class ChatMessage(models.Model):
    """Mensagens individuais trocadas em uma sessão de chat"""
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name="messages",
        verbose_name=_("Sessão")
    )
    is_user = models.BooleanField(_("Do usuário"), default=True)
    message = models.TextField(_("Mensagem"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    response = models.ForeignKey(
        BotResponse, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="generated_messages",
        verbose_name=_("Resposta associada")
    )
    
    class Meta:
        verbose_name = _("Mensagem de Chat")
        verbose_name_plural = _("Mensagens de Chat")
        ordering = ['session', 'timestamp']
    
    def __str__(self):
        sender = _("Usuário") if self.is_user else _("Bot")
        return f"{sender}: {self.message[:50]}..."