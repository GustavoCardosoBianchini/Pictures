'''
Serializers for Postagem API
'''

from django.utils.timezone import now
from rest_framework import serializers

from core.models import (ModelPostagem)


class PostagemSerializer(serializers.ModelSerializer):
    ''' Serializer for Postagens '''

    class Meta:
        model = ModelPostagem
        fields = ['id', 'txt_postagem']
        read_only_fields = ['id']

    def create(self, validated_data):
        '''create a postagem '''
        postagem = ModelPostagem.objects.create(**validated_data)

        return postagem

    # Since its a created object, we will work with it's instance as well
    def update(self, instance, validated_data):
        ''' update postagem'''
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostagemDetailSerializer(PostagemSerializer):
    """Serializer for recipe detail view"""

    # adiciona o campo description ao meta modelo
    class Meta(PostagemSerializer.Meta):
        fields = PostagemSerializer.Meta.fields