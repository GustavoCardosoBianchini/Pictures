'''
Vies for Postagem API
'''

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)
from rest_framework import (viewsets,
                            mixins,
                            status)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (ModelPostagem)
from postagem import serializers


class PostagemViewSets(viewsets.ModelViewSet):
    '''view for managing postagens API'''
    serializer_class = serializers.PostagemDetailSerializer

    # especifica qual o model de modelos que vamos usar para trabalhar
    queryset = ModelPostagem.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        '''convert a list of strings to Integers'''
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        '''Retrieve data for authenticated user'''
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        '''Return the serializer class for request'''
        if self.action == 'list':
            return serializers.PostagemSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        '''Create a new postagem'''
        serializer.save(user=self.request.user)

class BasePostagemAttrViewSet(mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    '''Base classe for attributes of recipes'''
    # deixe as informações genericas aqui.

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Retrive data for authenticated user'''
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()
