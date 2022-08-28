from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from reviews.models import Comment, Review
from reviews.models import Category, Title, Genre
from .serializers import CommentSerializers, ReviewSerializers
# from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from rest_framework import permissions
from api import serializers
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializers import GetTokenSerializer
from .serializers import UserSerializer, SignUpSerializer, UserAdminSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly
from .permissions import IsAuthorModeratorAdminOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = PageNumberPagination
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
    pagination_class = PageNumberPagination
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
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = serializers.TitleReadSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitleReadSerializer
        return serializers.TitleCreateSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        year = self.request.query_params.get('year')
        if year is not None:
            queryset = queryset.filter(year=year)
        category = self.request.query_params.get('category')
        if category is not None:
            category = Category.objects.all().filter(slug=category)
            category_id = category[0].id
            queryset = queryset.filter(category=category_id)
        genre = self.request.query_params.get('genre')
        if genre is not None:
            genre = Genre.objects.all().filter(slug=genre)
            genre_id = genre[0].id
            queryset = queryset.filter(genre=genre_id)
        return queryset


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
