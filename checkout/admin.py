from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'date', 'item_name', 'grand_total')
    list_filter = ('date', 'country')
    search_fields = ('full_name', 'email', 'item_name')
    readonly_fields = ('date', 'grand_total')

    fieldsets = (
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Address', {
            'fields': ('country', 'town_or_city', 'street_address1', 'street_address2', 'postal_code')
        }),
        ('Order Details', {
            'fields': ('item_name', 'item_price', 'grand_total', 'date')
        })
    )

admin.site.register(Order, OrderAdmin)