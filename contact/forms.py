from django import forms
from .models import ContactForm


class ContactForm(forms.ModelForm):
    name = forms.CharField(
            label='Name',
            max_length=100,
            widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
        )
    phonenumber = forms.CharField(
            label='Phone Number',
            max_length=20,
            required=False,
            widget=forms.TextInput(attrs={'placeholder':
                                   'phone number'})
        )
    email = forms.EmailField(
            label='Email',
            widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
        )
    message = forms.CharField(
            label='Message',
            widget=forms.Textarea(attrs={'placeholder':
                                         'Write your message here'})
        )

    # Contact from model ContactForm
    class Meta:
        model = ContactForm
        fields = ['name', 'phonenumber', 'email', 'message']
