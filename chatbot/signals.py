from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Avatar, Emotion, HUDSetting, BotResponse

# Chaves de cache
EMOTIONS_CACHE_KEY = 'emotions_data'
HUD_SETTINGS_CACHE_KEY = 'active_hud_settings'
AVATAR_CACHE_KEY = 'default_avatar'

@receiver([post_save, post_delete], sender=Emotion)
def update_emotions_cache(sender, **kwargs):
    """Atualiza o cache quando as emoções são modificadas"""
    cache.delete(EMOTIONS_CACHE_KEY)

@receiver([post_save, post_delete], sender=HUDSetting)
def update_hud_settings_cache(sender, **kwargs):
    """Atualiza o cache quando as configurações de HUD são modificadas"""
    cache.delete(HUD_SETTINGS_CACHE_KEY)

@receiver([post_save, post_delete], sender=Avatar)
def update_avatar_cache(sender, **kwargs):
    """Atualiza o cache quando os avatares são modificados"""
    cache.delete(AVATAR_CACHE_KEY)

@receiver(post_save, sender=BotResponse)
def update_response_related_caches(sender, instance, created, **kwargs):
    """Atualiza caches relacionados quando uma resposta é modificada"""
    # Limpar caches que possam conter dados de resposta
    cache.delete(f'category_responses_{instance.category_id}')