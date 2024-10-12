from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Meta:
        db_table = 'winday_user'  # Nombre de tabla personalizado

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='winday_user_groups',  # Cambiar related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='winday_user_permissions',  # Cambiar related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
