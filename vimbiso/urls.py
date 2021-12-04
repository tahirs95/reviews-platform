from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'vimbiso'
urlpatterns = [
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('plans/', plans, name='plans'),
    path('business/', business, name='business'),
    path('aboutus/', aboutus, name='aboutus'),
    path('add-review/', addReview, name='addReview'),
    path('addcategory/', AddCategory,name='AddCategory'),
    path('view-companies/', companies, name='companies'),
    path('view-companies-description/<int:id>/', company_description, name='company_description'),
    path('subscribe/', subscribe, name='subscribe'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)