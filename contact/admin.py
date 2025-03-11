from django.contrib import admin
from .models import ContactForm
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(ContactForm)
class ContactFormAdmin(SummernoteModelAdmin):
    list_display = ("name", "phonenumber", "email", "message")
    search_fields = ["name", "email"]