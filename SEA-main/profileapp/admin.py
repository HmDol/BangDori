from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, AbstractUser

from .models import Profile


# Register your models here.

admin.site.register(Profile)