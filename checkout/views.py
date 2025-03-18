import stripe
from django.conf import settings
from django.http import JsonResponse

def test_stripe(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Test request to retrieve account details
        account = stripe.Account.retrieve()
        return JsonResponse(account)
    except stripe.error.AuthenticationError as e:
        return JsonResponse({'error': f"Authentication error: {str(e)}"})
    except Exception as e:
        return JsonResponse({'error': f"Error: {str(e)}"})

import stripe

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import OrderForm
from .models import Order

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    stripe.api_key = stripe_secret_key

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                # Create order first with form data
                order = form.save(commit=False)
                order.item_name = "Fixed Price Item"
                order.item_price = 50.00
                order.grand_total = 50.00

                # Create Stripe PaymentIntent
                stripe.api_key = stripe_secret_key
                intent = stripe.PaymentIntent.create(
                    amount=5000,  # 50.00 EUR
                    currency='eur',
                    payment_method_types=['card'],
                    metadata={
                        'order_id': order.id,
                        'email': order.email
                    }
                )
                # Print the client secret to verify its format
                print(intent.client_secret)

                # Link Stripe payment ID to order
                order.stripe_pid = intent.id
                order.save()

                return render(request, 'checkout/payment.html', {
                    'client_secret': intent.client_secret,
                    'stripe_public_key': stripe_public_key,
                    'order': order,
                })

            except stripe.error.StripeError as e:
                messages.error(request, f"Payment error: {str(e)}")
                return redirect('checkout')

            except Exception as e:
                messages.error(request, f"Error processing order: {str(e)}")
                return redirect('checkout')

    else:
        form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'fixed_price': 50.00,
    }

    return render(request, template, context)