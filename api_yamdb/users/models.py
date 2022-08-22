from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'user'),
    ('admin', 'admin'),
    ('moderator', 'moderator')
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.SlugField(
        'Роль',
        choices=ROLES,
        default='user'
    )
