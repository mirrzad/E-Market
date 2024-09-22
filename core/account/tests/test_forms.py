from django.test import TestCase
from account.forms import UserRegistrationForm
from account.models import User


class TestUserRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            phone_number='09131234567',
            email='admin@email.com',
            password='Admin@2023',
        )

    def test_valid_data(self):
        form = UserRegistrationForm(data={'phone_number': '09137654321', 'email': 'amir@email.com',
                                    'password1': 'Root@2023', 'password2': 'Root@2023'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertTrue(len(form.errors), 4)
        self.assertFalse(form.is_valid())

    def test_email_exists(self):
        form = UserRegistrationForm(data={'phone_number': '09131234789', 'email': 'admin@email.com',
                                    'password1': 'Root@2023', 'password2': 'Root@2023'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_phone_number_exists(self):
        form = UserRegistrationForm(data={'phone_number': '09131234567', 'email': 'amir@email.com',
                                    'password1': 'Root@2023', 'password2': 'Root@2023'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('phone_number'))

    def test_unmatched_password(self):
        form = UserRegistrationForm(data={'phone_number': '09137654321', 'email': 'amir@email.com',
                                          'password1': 'Root@2023', 'password2': 'Root@2025'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)

