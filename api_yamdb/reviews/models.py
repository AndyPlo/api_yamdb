from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    genres = models.ManyToManyField(
        Genre,
        through='Genre_title'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Genre_title(models.Model):
    title_id = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='titles'
    )
    genre_id = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genres'
    )

    def __str__(self):
        return f'{self.title_id.name} - {self.genre_id.name}'

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='unique_combination'
            )
        ]


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.text)[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.text)[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментрий'
        verbose_name_plural = 'Комментарии'
