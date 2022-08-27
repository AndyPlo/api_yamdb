from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'user'),
    ('admin', 'admin'),
    ('moderator', 'moderator')
]


class User(AbstractUser):
    username = models.SlugField(max_length=150, unique=True)
    email = models.EmailField(max_length=254)
    bio = models.TextField(blank=True)
    role = models.SlugField(choices=ROLES, default='user')
    confirmation_code = models.SlugField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]
