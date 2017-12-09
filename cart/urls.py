from django.conf.urls import path
from . import views

urlpatterns = [
    path('mycart', views.cart, name='mycart'),
]