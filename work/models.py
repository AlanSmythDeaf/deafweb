# models.py
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Website(models.Model):
    CATEGORY_CHOICES = [
        ('charity', 'Charity'),
        ('retail', 'Retail'),
        ('service', 'Service'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
