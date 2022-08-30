# Generated by Django 2.2.16 on 2022-08-30 17:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220828_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review', verbose_name='Отзыв'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='genre_title',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='genres', to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='genre_title',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.Title', verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Отзыв'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title', verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='reviews.Genre_title', to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(2022)], verbose_name='Год выпуска'),
        ),
    ]