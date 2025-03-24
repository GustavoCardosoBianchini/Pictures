"""
test de funções de admin, para pagina web admin na web
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from rest_framework import status

class AdminTest(TestCase):
    ''' test the admin process '''

    def setUp(self):
        '''create base superuser'''
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='pas123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='normalguy@example.com',
            password='pas456',
            name='jorge'
        )

    def test_users_list(self):
        '''teste lists user'''
        url = reverse('admin:core_modeluser_changelist')
        res =self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        '''test modify user page'''
        url = reverse('admin:core_modeluser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_page(self):
        '''teste para criar a pagina de criar usuario.'''

        url = reverse('admin:core_modeluser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)