from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Avatar, Emotion, ResponseCategory, BotResponse, GameCommand

class AvatarForm(forms.ModelForm):
    """Formulário para gerenciar avatares do bot"""
    class Meta:
        model = Avatar
        fields = ['name', 'model_url', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EmotionForm(forms.ModelForm):
    """Formulário para gerenciar emoções do bot"""
    class Meta:
        model = Emotion
        fields = ['name', 'animation_name', 'expression_name', 'expression_intensity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'animation_name': forms.TextInput(attrs={'class': 'form-control'}),
            'expression_name': forms.TextInput(attrs={'class': 'form-control'}),
            'expression_intensity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

class ResponseCategoryForm(forms.ModelForm):
    """Formulário para gerenciar categorias de resposta"""
    class Meta:
        model = ResponseCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BotResponseForm(forms.ModelForm):
    """Formulário para gerenciar respostas do bot"""
    class Meta:
        model = BotResponse
        fields = ['category', 'trigger_keywords', 'response_text', 'emotion', 'priority', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'trigger_keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Palavras-chave separadas por vírgula'}),
            'response_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'emotion': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GameCommandForm(forms.ModelForm):
    """Formulário para gerenciar comandos de jogo"""
    class Meta:
        model = GameCommand
        fields = ['name', 'command_type', 'trigger_keywords', 'response_text', 'emotion', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'command_type': forms.Select(attrs={'class': 'form-select'}),
            'trigger_keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Palavras-chave separadas por vírgula'}),
            'response_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'emotion': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }