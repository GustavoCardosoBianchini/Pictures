'''
serialiazers process the api data
'''

from django.contrib.auth import (
                                get_user_model,
                                authenticate
                                )

from django.utils.translation import gettext as _, trim_whitespace

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password':{'write_only':True, 'min_length':5}}

    def create(self, validated_data):
        ''' create and return user with encripted password'''
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthenticateUserSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False
    )

    def validate(self, attrs):
        ''' validate and authenticate user'''
        user = authenticate(
            request= self.context.get('request'),
            username = attrs.get('email'),
            password = attrs.get('password')
        )

        if not user:
            msg= _('Invalid Credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs