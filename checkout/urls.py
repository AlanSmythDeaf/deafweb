from django.urls import path
from . import views
from .webhooks import webhooks

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout/success/<int:order_id>/', views.checkout_success,
         name='checkout_success'),
    path('wh/', webhooks, name='webhooks'),
]
