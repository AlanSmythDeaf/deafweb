from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',  
            'town_or_city', 'country'  
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['autofocus'] = True

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postal_code': 'Postal Code',
            'country': 'Country',
        }

        for field_name, placeholder_text in placeholders.items():
            field = self.fields.get(field_name)
            if field:
                required = field.required
                field.widget.attrs['placeholder'] = (
                    f"{placeholder_text}{' *' if required else ''}"
                )
                field.widget.attrs['class'] = 'form-control'
                field.label = False

