'''
views send the response to the backend to process
'''
from django.contrib.auth import authenticate
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (UserSerializer, AuthenticateUserSerializer)

class CreateUserView(generics.CreateAPIView):
    '''Create a new user in the system '''
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    '''Create a new token '''
    serializer_class = AuthenticateUserSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the user in the system"""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes =  [permissions.IsAuthenticated]

    def get_object(self):
        ''' return authenticated user '''
        return self.request.user
