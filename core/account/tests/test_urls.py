from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import UserRegistrationView, UserLoginView, UserLogoutView


class TestUrls(SimpleTestCase):
    def test_register_url(self):
        url = reverse('account:user-register')
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    def test_login_url(self):
        url = reverse('account:user-login')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_logout_url(self):
        url = reverse('account:user-logout')
        self.assertEqual(resolve(url).func.view_class, UserLogoutView)
