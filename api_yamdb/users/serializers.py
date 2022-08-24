from rest_framework import serializers, validators
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


class TokenSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['password'].required = False

    def validate(self, attrs):
        # attrs.update({'password': ''})
        return super(TokenSerializer, self).validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
