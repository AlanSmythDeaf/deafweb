from django.contrib import admin
from .models import Category, Website


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url')
    search_fields = ['name']


admin.site.register(Category)
admin.site.register(Website, WebsiteAdmin)
