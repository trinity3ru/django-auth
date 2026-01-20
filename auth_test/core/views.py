from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm

# Главная страница, откуда пользователь переходит к регистрации или входу; не содержит чувствительных данных.
def home_view(request):
    return render(request, 'core/home.html')


# Профиль отображается только авторизованному пользователю и показывает базовую информацию из объекта user.
@login_required
def profile_view(request):
    return render(request, 'core/profile.html')


# Регистрация использует встроенную форму UserCreationForm, чтобы не изобретать свою логику валидации.
# После успешного сохранения пользователя сразу логиним его и перенаправляем на профиль.
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


# Простейший logout: вызываем встроенную функцию logout и перенаправляем на главную.
def logout_view(request):
    logout(request)
    return redirect('core:home')
