from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Comment, Review
from reviews.models import Category, Title, Genre
from .serializers import CommentSerializers, ReviewSerializers
# from django.shortcuts import render
from rest_framework import viewsets, filters, mixins, validators
from rest_framework import permissions
from api import serializers
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializers import GetTokenSerializer, UserProfileSerializer
from .serializers import UserSerializer, SignUpSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly
from .permissions import IsAuthorModeratorAdminOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    queryset = Review.objects.all()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleReadSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('name', 'year', 'category')

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitleReadSerializer
        return serializers.TitleCreateSerializer


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
                {'user'}
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)


class GetTokenView(TokenObtainPairView):
    serializer_class = GetTokenSerializer
