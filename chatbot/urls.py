from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/process-message/', views.process_message, name='process_message'),
    path('api/save-username/', views.save_username, name='save_username'),
    path('api/end-session/', views.end_session, name='end_session'),
    path('api/hud-settings/', views.get_hud_settings, name='hud_settings'),
]