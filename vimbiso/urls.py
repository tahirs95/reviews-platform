from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'vimbiso'
urlpatterns = [
    path('', index, name='index'),
    path('categories', categories, name='categories'),
    path('plans', plans, name='plans'),
    path('business', business, name='business'),
]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)