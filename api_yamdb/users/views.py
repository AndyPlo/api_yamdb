from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import User
from .serializers import UserSerializer, SignUpSerializer
from api.permissions import IsAdmin
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = User.objects.filter(pk=self.request.user.pk)
        return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(username=serializer.validated_data['username'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Confirmation code',
            (f'Confirmation code for {user}'
             f' is: {confirmation_code[29:]}'),
            'from@example.com',
            [serializer.validated_data['email']]
        )
