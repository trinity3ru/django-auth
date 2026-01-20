from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации для кастомной модели пользователя."""

    class Meta:
        model = CustomUser
        fields = ('username', 'phone', 'email')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and not phone.isdigit():
            raise forms.ValidationError('Телефон может содержать только цифры.')
        return phone
