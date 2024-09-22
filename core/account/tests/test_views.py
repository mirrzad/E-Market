from django.test import TestCase, Client
from django.urls import reverse
from account.forms import UserRegistrationForm
from account.models import User
from account.views import UserLogoutView


class TestUserRegistrationView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse('account:user-register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register-user.html')
        self.assertEqual(response.context['form'], UserRegistrationForm)

    def test_user_register_POST_valid(self):
        response = self.client.post(reverse('account:user-register'), data={
            'phone_number': '09131234567',
            'email': 'admin@email.com',
            'password1': 'Root@2023',
            'password2': 'Root@2023',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:verify-register-code'))

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('account:user-register'), data={
            'phone_number': '09131234567',
            'email': 'invalid email',
            'password1': 'Root@2023',
            'password2': 'Root@2023',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response.context['form'], field='email', errors=['Enter a valid email address.'])


class TestUserLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09131234567',
            email='admin@email.com',
            password='Root@2023',
        )
        self.client = Client()
        self.client.login(phone_number='09131234567', password='Root@2023')
        self.client2 = Client()

    def test_user_logout_GET(self):
        response = self.client.get(reverse('account:user-logout'))
        self.assertRedirects(response, reverse('home:home-page'))

    def test_user_logout_anonymous(self):
        res = self.client2.get(reverse('account:user-logout'))
        self.assertEqual(res.status_code, 302)
