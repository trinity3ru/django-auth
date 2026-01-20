from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

# Простые маршруты отвечают за главную страницу, профиль и формы регистрации/входа/выхода.
app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('signup/', views.signup_view, name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html', next_page='core:home'),
        name='login',
    ),
    path('logout/', views.logout_view, name='logout'),
]
