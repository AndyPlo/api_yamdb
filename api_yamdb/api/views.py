from unicodedata import name
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from reviews.models import Category, Title, Genre
from api import serializers


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination

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
