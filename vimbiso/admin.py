from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib.auth.admin import UserAdmin
from django.contrib import auth
from .models import *

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ["username", "is_superuser", 'contact', 'address', 'email','level']

admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(BusinessProfile)
