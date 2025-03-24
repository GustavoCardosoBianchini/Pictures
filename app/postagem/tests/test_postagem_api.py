'''
tests for postagem API
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import ModelPostagem

from postagem.serializers import PostagemSerializer, PostagemDetailSerializer

POSTAGEM_URL = reverse('postagem:modelpostagem-list')

def detail_url(postagem_id):
    '''Create a detail url of the postagem'''
    return reverse('postagem:modelpostagem-detail', args=[postagem_id])

def create_user(email, password='pass1234'):
    user = get_user_model().objects.create_user(email, password)
    return user

def create_postagem(user, txt):
    postagem = ModelPostagem.objects.create(user=user,
                                       txt_postagem=txt)

    return postagem

class PublicPostagemAPI(TestCase):
    '''class to test unauthenticated api calls'''

    def setUp(self):
        self.client = APIClient()

    def test_unathenticated_postagem(self):
        '''test to create a postagem with unauthenticated user'''

        res = self.client.get(POSTAGEM_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatePostagemAPI(TestCase):
    '''class to test authenticated api calls'''

    def setUp(self):
        self.client = APIClient()
        self.user = create_user('ricardo@example.com')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_postagem(self):
        '''test retrieving a list of postagens'''
        create_postagem(self.user,'texte example 1')
        create_postagem(self.user, 'texte example 2')

        res = self.client.get(POSTAGEM_URL)

        postagem = ModelPostagem.objects.all().order_by('-id')
        serializer = PostagemSerializer(postagem, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_listing_postagem_by_user(self):
        '''test to return only the postagem of the user'''
        other_user = get_user_model().objects.create_user(email='keila@example.com',
                                                          password='pass12345')
        create_postagem(other_user,'text_example3')

        create_postagem(self.user,'text_example1')
        create_postagem(self.user,'text_example2')

        res = self.client.get(POSTAGEM_URL)

        postagem = ModelPostagem.objects.all().order_by('-id')
        serializer = PostagemSerializer(postagem, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(res.data, serializer.data)

    def test_detail_postagem(self):
        '''test the details of postagem'''
        postagem = create_postagem(self.user, 'text_exaple1')

        url = detail_url(postagem.id)
        res = self.client.get(url)

        serializer = PostagemDetailSerializer(postagem)
        self.assertEqual(res.data, serializer.data)

    def test_authenticated_postagem(self):
        '''test to create a postagem with authenticated user'''
        payload = {'user': self.user,
                   'txt_postagem': 'Essa é a postagem de teste'}

        res = self.client.post(POSTAGEM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        postagens = ModelPostagem.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(postagens, k), v)
        self.assertEqual(postagens.user, self.user)

    def test_patch_postagem(self):
        '''test patch a postagem'''
        postagem = create_postagem(self.user, 'text_example1')

        payload={
            'txt_postagem': 'new text_example2'
        }

        url = detail_url(postagem.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['txt_postagem'], payload['txt_postagem'])
        self.assertEqual(postagem.user, self.user)

    def test_delete_postagem(self):
        '''test delete a postagem'''
        postagem = create_postagem(self.user, 'text_example1')
        create_postagem(self.user, 'text_example2')

        url = detail_url(postagem.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        user_postagens = ModelPostagem.objects.filter(user=self.user)
        self.assertFalse(user_postagens.filter(id=postagem.id).exists())


