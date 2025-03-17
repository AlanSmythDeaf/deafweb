import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import OrderForm
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.item_name = "Fixed Price Item"
            order.item_price = 50.00
            order.grand_total = 50.00

            intent = stripe.PaymentIntent.create(
                amount=5000,  # Amount in cents
                currency='eur',
            )

            order.stripe_pid = intent.id
            order.save()

            context = {
                'form': form,
                'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
                'client_secret': 'test_secret',
            }
            return render(request, 'checkout/checkout.html', context)

    else:
        form = OrderForm()

    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'client_secret': 'intent.client_secret',
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request):
    """Handle successful checkouts"""
    return render(request, 'checkout/success.html')

def checkout_cancel(request):
    """Handle canceled checkouts"""
    return render(request, 'checkout/cancel.html')