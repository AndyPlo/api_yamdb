import datetime as dt
import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Genre_title, Review, Title
from users.models import User


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка может быть только от 1 до 10!'
            )
        return value

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title).exists():
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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
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
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return round(rating, 1) if rating else rating


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
                genre=current_genre[0],
                title=title
            )
        return (title)

    def validate_year(self, value):
        year = dt.date.today().year
        if (value > year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        ordering = ['-username']
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        if self.initial_data.get('username') == 'me':
            raise serializers.ValidationError(
                {"username": ["Вы не можете использоват этот username!"]}
            )
        if User.objects.filter(
            username=self.initial_data.get('username')
        ).exists():
            raise serializers.ValidationError(
                {"username": ["Этот username уже зарегистрирован!"]}
            )
        if User.objects.filter(
            email=self.initial_data.get('email')
        ).exists():
            raise serializers.ValidationError(
                {"email": ["Этот email уже зарегистрирован!"]}
            )
        return data


class UserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        ordering = ['-username']
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        if self.initial_data.get('username') == 'me':
            raise serializers.ValidationError(
                {"username": ["Вы не можете использоват этот username!"]}
            )
        if User.objects.filter(
            username=self.initial_data.get('username')
        ).exists():
            raise serializers.ValidationError(
                {"username": ["Этот username уже зарегистрирован!"]}
            )
        if User.objects.filter(
            email=self.initial_data.get('email')
        ).exists():
            raise serializers.ValidationError(
                {"email": ["Этот email уже зарегистрирован!"]}
            )
        return data


class SignUpSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['email'] = serializers.EmailField()

    def validate(self, attrs):
        if self.initial_data.get('username') == 'me':
            raise serializers.ValidationError(
                {"username": ["Вы не можете использоват этот username!"]}
            )
        if User.objects.filter(
            username=self.initial_data.get('username')
        ).exists():
            raise serializers.ValidationError(
                {"username": ["Этот username уже зарегистрирован!"]}
            )
        if User.objects.filter(
            email=self.initial_data.get('email')
        ).exists():
            raise serializers.ValidationError(
                {"email": ["Этот email уже зарегистрирован!"]}
            )
        return attrs

    def create(self, validated_data):
        confirmation_code = str(uuid.uuid4()).split("-")[0]
        user = User.objects.filter(
            username=validated_data['username'],
            email=validated_data['email']
        )
        if user.exists():
            user.update(confirmation_code=confirmation_code)
        else:
            User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                confirmation_code=confirmation_code
            )
        send_mail(
            'Код подтверждения',
            (f'Код подтверждения для пользователя "{user[0].username}":'
                f' {confirmation_code}'),
            'from@example.com',
            [validated_data['email']]
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
        if attrs['confirmation_code'] == self.user.confirmation_code:
            refresh = RefreshToken.for_user(self.user)
            return {'token': str(refresh.access_token)}
        raise exceptions.ValidationError(
            'Проверьте правильность указанных для получения токена данных.'
        )
