# Generated by Django 2.2.16 on 2022-08-28 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220827_2153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre_title',
            old_name='genre_id',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='genre_title',
            old_name='title_id',
            new_name='title',
        ),
    ]
