from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('test-stripe/', views.test_stripe, name='test_stripe'),
]