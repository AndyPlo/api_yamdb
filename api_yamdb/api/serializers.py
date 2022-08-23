from dataclasses import fields
from rest_framework import serializers

from reviews.models import Category, Title, Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug',)
        lookup_field = 'id'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug',)
        lookup_field = 'id'
