from rest_framework import serializers, validators, exceptions
from reviews.models import Comment, Review
from reviews.models import Category, Genre_title, Title, Genre
import datetime as dt
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import uuid
from django.core.mail import send_mail
# from rest_framework import status
# from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if not 1 < data['score'] < 10:
            raise serializers.ValidationError(
                'Оценка может быть только от 1 до 10!'
            )
        return data['score']

    def validate_author_nomore(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'id'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )

    def get_rating(self, obj):
        title_reviews = Review.objects.all().filter(
            title_id=obj.id
        )
        if not title_reviews:
            return 0
        rating = 0
        for title_review in title_reviews:
            rating += title_review.score
        return (rating)


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )

    def get_rating(self, obj):
        return 0

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genre.objects.all().filter(
                name=genre.name
            )
            Genre_title.objects.create(
                genre_id=current_genre[0],
                title_id=title
            )
        # response_title = Title.objects.all().filter(id=title.id)
        return (title)

    def validate_year(self, value):
        year = dt.date.today().year
        if (value > year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('role',)
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


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
                {"username": ["You cannot use this username!"]}
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
                {"username": ["You cannot use this username!"]}
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
        self.user = get_object_or_404(User, username=attrs['username'])
        try:
            if attrs['confirmation_code'] == self.user.confirmation_code:
                refresh = RefreshToken.for_user(self.user)
                return {'token': str(refresh.access_token)}
        except Exception:
            raise exceptions.AuthenticationFailed(
                'No active account found with the given credentials.'
            )
