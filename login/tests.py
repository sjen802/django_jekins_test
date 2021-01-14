from django.test import TestCase
from django.test import client
from login import models
from django.contrib.auth.models import User

class LoginTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('user', email='user@example.com', password = 'abcde')
        self.c = client.Client()

    def test_register(self):

        self.c.post('api/register/', {'username': 'user', 'password': 'abcde'}, follow=True)