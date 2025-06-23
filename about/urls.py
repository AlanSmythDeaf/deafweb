from django.urls import path
from .views import about, manage_faq, delete_faq, edit_faq

urlpatterns = [
    path('', about, name='about'),
    path('manage-faq/', manage_faq, name='manage_faq'),
    path('delete-faq/<int:faq_id>/', delete_faq, name='delete_faq'),
    path('edit-faq/<int:faq_id>/', edit_faq, name='edit_faq'),
]

