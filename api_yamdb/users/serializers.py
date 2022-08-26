from rest_framework import serializers, validators, exceptions
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate(self, data):
        if self.initial_data['username'] == 'me':
            raise serializers.ValidationError(
                'You cannot use this username!'
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate(self, data):
        if self.initial_data['username'] == 'me':
            raise serializers.ValidationError(
                'You cannot use this username!'
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()

    def validate(self, attrs):
        try:
            self.user = User.objects.get(username=attrs['username'])
        except Exception:
            raise exceptions.AuthenticationFailed(
                'No active account found with the given credentials!'
            )
        refresh = RefreshToken.for_user(self.user)
        return {'token': str(refresh.access_token)}
