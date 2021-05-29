from django.urls import path, include, re_path
from .views import *

app_name = 'users'


urlpatterns = [
    path('', index, name="index"),

]