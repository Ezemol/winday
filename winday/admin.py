from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Place, Favorite, Profile

admin.site.register(Place)
admin.site.register(Favorite)
admin.site.register(Profile)