from django.db import models

# Create your models here.


class Order(models.Model):

    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ]

    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    item_name = models.CharField(max_length=100, null=False, blank=False)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f"Thank you {self.full_name}"