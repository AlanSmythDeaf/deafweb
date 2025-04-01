from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# Create views here.


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent!')

            return render(request, 'contact/thank_you.html')
        else:
            messages.error(request, 'Error sending message')

    else:
        return render(request, 'contact/contact.html', {'form': form})
