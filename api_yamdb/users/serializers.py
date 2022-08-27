from rest_framework import serializers, validators, exceptions
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import uuid
from django.core.mail import send_mail


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


class SignUpSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['email'] = serializers.EmailField()

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                'You cannot use this username!'
            )
        return attrs

    def create(self, validated_data):
        confirmation_code = str(uuid.uuid4()).split("-")[0]
        user = User.objects.filter(
            username=validated_data['username'],
            email=validated_data['email']
        )
        try:
            if user.exists():
                user.update(confirmation_code=confirmation_code)
            else:
                User.objects.create(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    confirmation_code=confirmation_code
                )
            send_mail(
                'Confirmation code',
                (f'Confirmation code for "{user[0].username}" is:'
                 f' {confirmation_code}'),
                'from@example.com',
                [validated_data['email']]
            )
        except Exception:
            raise serializers.ValidationError(
                'No active account found with the given credentials.'
            )
        return validated_data

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.SlugField()

    def validate(self, attrs):
        try:
            self.user = User.objects.get(username=attrs['username'])
            if attrs['confirmation_code'] == self.user.confirmation_code:
                refresh = RefreshToken.for_user(self.user)
                return {'token': str(refresh.access_token)}
        except Exception:
            raise exceptions.AuthenticationFailed(
                'No active account found with the given credentials.'
            )
