from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):

    readonly_fields = ('order_number',
                       'grand_total',)

    fields = ('date', 'full_name',
              'email', 'phone_number', 'country',
              'town_or_city', 'street_address1',
              'street_address2', 'grand_total',)

    list_display = ('order_number', 'date', 'full_name',
                    'delivery_cost',
                    'grand_total',)

admin.site.register(Order)