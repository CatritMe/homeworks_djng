from django.urls import path

from catalog.apps import MainConfig
from catalog.views import home, contacts, products

app_name = MainConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/<int:pk>/', products, name='products'),
]