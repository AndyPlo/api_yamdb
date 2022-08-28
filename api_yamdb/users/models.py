from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'user'),
    ('admin', 'admin'),
    ('moderator', 'moderator')
]


class User(AbstractUser):
    username = models.SlugField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    role = models.SlugField(choices=ROLES, default='user')
    confirmation_code = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['-username']
