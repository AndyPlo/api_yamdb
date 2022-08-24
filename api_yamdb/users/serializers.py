from rest_framework import serializers, validators
from .models import User


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
