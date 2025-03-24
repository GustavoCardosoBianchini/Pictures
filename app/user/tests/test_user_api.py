'''
Test user API
'''
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    '''helper function to create new test user'''
    return get_user_model().objects.create_user(**params)

class PublicUserAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_API(self):
        ''' test create new user using API '''
        payload ={
            'email': 'eduardo@example.com',
            'password': 'teste@123',
            'name': "Eduardo"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_create_user_with_existing_email(self):
        ''' teste don't let it create a new user with existing email '''
        create_user(email='gustavo@exemaple.com',
                    password='pas123',
                    name='Carlos')

        payload = {
            'email':'gustavo@exemaple.com',
            'password':'pas123',
            'name':'gustavo'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email':'jorge@example.com',
            'password':'pw',
            'Name':'Jorge',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''test create new token for user '''
        create_user(email='gustavo@exemaple.com',
                    password='pas123',
                    name='Carlos')

        payload ={
            'email':'gustavo@exemaple.com',
            'password':'pas123'
        }

        res = self.client.post(CREATE_TOKEN, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_failed_to_authenticate(self):
        create_user(email='gustavo@exemaple.com',
                    password='pas123',
                    name='Carlos')

        payload = {
            'email': 'gustavo@exemaple.com',
            'password': '123pass'
        }

        res = self.client.post(CREATE_TOKEN, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_token_with_blank_pass(self):
        '''teste blank password'''
        create_user(email='gustavo@exemaple.com',
                    password='pas123',
                    name='Carlos')

        payload = {
            'email': 'gustavo@exemaple.com',
            'password': ''
        }

        res = self.client.post(CREATE_TOKEN, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_unauthorized(self):
        ''' test request for authenticated users '''

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateUserAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='keila@example.com',
                                password='pas123',
                                name='keila')
        self.client.force_authenticate(user=self.user)

    def test_retrive_authenticated_user(self):
        '''test to retrieve authenticated user '''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email':self.user.email,
            'name':self.user.name,
        })

    def test_patch_authenticated_user(self):
        ''' test to patch authenticate user'''
        payload={'name':'jorge'}

        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])


    def test_update_authenticated_user(self):
        ''' test to update authenticated user'''
        payload={'email': 'jorge@example.com',
                 'password': 'pas567',
                 'name':'jorge'
                 }

        res = self.client.put(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))


