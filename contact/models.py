from django.db import models

# Create your models here.

class ContactForm(models.Model):
    name = models.CharField(max_length=200, blank=False)
    phonenumber = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=False)
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"