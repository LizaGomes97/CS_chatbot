from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
    verbose_name = _('Chatbot CS')
    
    def ready(self):
        # Importar sinais
        from . import signals