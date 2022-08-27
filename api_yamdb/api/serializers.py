from rest_framework import serializers
from rest_framework.response import Response

import datetime as dt

from reviews.models import Category, Genre_title, Title, Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'id'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    '''genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )'''

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            #'genre',
        )

    def create(self, validated_data):
        #category_data = validated_data.pop('category')
        #genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        '''for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            Genre_title.objects.create(
                genre_id=current_genre,
                title_id=title.id
            )'''
        serializer = TitleReadSerializer(title)
        return Response(serializer.data)

    def validate_year(self, value):
        year = dt.date.today().year
        if (value > year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value
