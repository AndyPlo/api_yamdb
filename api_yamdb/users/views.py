from rest_framework import viewsets, mixins, validators
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import User
from .serializers import GetTokenSerializer, UserProfileSerializer
from .serializers import UserSerializer, SignUpSerializer
from api.permissions import IsAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from http import HTTPStatus


class UserProfileViewSet(mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = User.objects.filter(pk=self.request.user.pk)
        return user

    def patch(self, request):
        if 'role' in request.data:
            raise validators.ValidationError(
                {"role": ["You cannot change this field."]}
            )
        user = User.objects.filter(pk=self.request.user.pk)
        user.update(**request.data)
        return Response(request.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignUpSerializer

    def retrieve(self, request):
        return Response(request, status=HTTPStatus.OK)


class GetTokenView(TokenObtainPairView):
    serializer_class = GetTokenSerializer
