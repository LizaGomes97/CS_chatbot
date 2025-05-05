from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chatbot.admin_views import admin_dashboard

# Customizar o site do admin
admin.site.site_header = 'Administração do CS Chatbot'
admin.site.site_title = 'CS Chatbot Admin'
admin.site.index_title = 'Painel de Controle'

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),
]

# Adicionar URLs para servir arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)