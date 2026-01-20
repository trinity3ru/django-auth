from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser
from django.test import TestCase
from django.urls import reverse


# Проверяем, что встроенная форма регистрации создаёт пользователя и перенаправляет на профиль.
class AuthCreationTests(TestCase):
    def test_signup_creates_user_and_redirects(self):
        signup_url = reverse('core:signup')
        response = self.client.post(
            signup_url,
            {
                'username': 'tester',
                'phone': '79990001122',
                'email': 'tester@example.com',
                'password1': 'strong-password-123!',
                'password2': 'strong-password-123!',
            },
            follow=True,
        )
        # Убедимся, что редирект идёт на страницу профиля и пользователь появился в базе.
        self.assertRedirects(response, reverse('core:profile'))
        user = CustomUser.objects.get(username='tester')
        self.assertEqual(user.phone, '79990001122')




# Проверяем классический цикл входа, выхода и защиту профиля.
class AuthSessionTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='cycle', phone='70000000000', email='cycle@example.com', password='cycle-pass-1'
        )

    def test_login_logout_and_profile_guard(self):
        login_url = reverse('core:login')
        profile_url = reverse('core:profile')
        logout_url = reverse('core:logout')

        # Выполняем вход и проверяем, что в сессии появился идентификатор пользователя.
        response = self.client.post(
            login_url,
            {'username': self.user.username, 'password': 'cycle-pass-1'},
            follow=True,
        )
        self.assertEqual(
            str(self.user.pk),
            self.client.session[SESSION_KEY],
        )

        # После входа профиль должен отдавать 200.
        profile_response = self.client.get(profile_url)
        self.assertEqual(profile_response.status_code, 200)

        # Выходим и убеждаемся, что представление возвращает редирект.
        logout_response = self.client.get(logout_url)
        self.assertEqual(logout_response.status_code, 302)
        # Очистим сессию через клиент, чтобы проверить поведение login_required.
        self.client.logout()
        post_logout_response = self.client.get(profile_url)
        expected_login_redirect = f"{login_url}?next={profile_url}"
        self.assertRedirects(post_logout_response, expected_login_redirect)
