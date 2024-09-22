from django.test import TestCase
from account.models import User
from model_bakery import baker


class TestUserModel(TestCase):
    def setUp(self):
        self.user = baker.make(User, email='admin@email.com')

    def test_str_method(self):
        self.assertEqual(str(self.user), 'admin@email.com')
