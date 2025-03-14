from django.urls import path
from .views import collaborate

urlpatterns = [
    path('', collaborate, name='collaborate'),
]