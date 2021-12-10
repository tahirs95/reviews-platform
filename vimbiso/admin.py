from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
import django.contrib.auth.admin
from django import forms
import django.contrib.auth.models
from django.contrib.auth.admin import UserAdmin
from django.contrib import auth
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

User = get_user_model()
password = User.objects.make_random_password()

class UserCreationForm(DjangoUserCreationForm):
    password1 = None
    password2 = None
    def clean(self):
        self.cleaned_data['password1'] = password
        self.cleaned_data['password2'] = password

        return super().clean()

@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ["username", "is_superuser", 'contact', 'address', 'email','level']
    # fieldsets = (
    #     (None, {'fields': ('username',)}),
    #     (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    # )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email'),
        }),
    )
    list_filter = tuple()

admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Tags)
admin.site.register(BusinessProfile)
