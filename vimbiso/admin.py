from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from import_export.admin import ImportExportModelAdmin
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
from import_export import resources

User = get_user_model()
password = User.objects.make_random_password()

class UserCreationForm(DjangoUserCreationForm):
    password1 = None
    password2 = None
    def clean(self):
        self.cleaned_data['password1'] = password
        self.cleaned_data['password2'] = password

        return super().clean()

# class CompanyResource(resources.ModelResource):

#     class Meta:
#         model = User

@admin.register(User)
class UserAdmin(UserAdmin,ImportExportModelAdmin):
    add_form = UserCreationForm
    list_display = ["username", "is_superuser", 'contact',  'email','level']
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
    # resource_class = CompanyResource




admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Tags)
admin.site.register(BusinessProfile)
admin.site.register(Subscription)
