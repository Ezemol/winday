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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    followers = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def serialize(self):
        return {
            "user": self.user.username,
            "followers_count": self.followers.count(),
            "following_count": self.user.following.count(),
        }
    
class Place(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'place')
        
        def __str__(self):
            return f"{self.user.username} - {self.place.name}"