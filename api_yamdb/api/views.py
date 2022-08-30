import uuid

from api import serializers
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from api_yamdb.settings import ADMIN_EMAIL

from .filters import TitleFilter
from .permissions import IsAdmin, IsAuthorModeratorAdminOrReadOnly, ReadOnly
from .serializers import (CommentSerializers, GetTokenSerializer,
                          ReviewSerializers, SignUpSerializer,
                          UserAdminSerializer, UserSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          IsAuthenticatedOrReadOnly)
    queryset = Review.objects.all()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          IsAuthenticatedOrReadOnly)
    queryset = Comment.objects.all()

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitleReadSerializer
        return serializers.TitleCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            pagination_class=None)
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(TokenObtainPairView):
    serializer_class = GetTokenSerializer


@api_view(['POST'])
def signup(request):
    user = User.objects.filter(**request.data)
    if user.exists():
        get_and_send_confirmation_code(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.filter(**serializer.data)
        get_and_send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_and_send_confirmation_code(user):
    confirmation_code = str(uuid.uuid4()).split("-")[0]
    user.update(confirmation_code=confirmation_code)
    send_mail(
        'Код подтверждения',
        (f'Код подтверждения для пользователя "{user[0].username}":'
            f' {user[0].confirmation_code}'),
        ADMIN_EMAIL,
        [user[0].email]
    )
