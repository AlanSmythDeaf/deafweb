from django.contrib import admin
from .models import ContactForm
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(ContactForm)
class ContactFormAdmin(SummernoteModelAdmin):
    list_display = ("name", "phonenumber", "email", "message")
    search_fields = ["name", "email"]

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only in the admin interface.
        """
        if obj:  # When editing an existing object
            return [field.name for field in self.model._meta.fields]
        return self.readonly_fields
