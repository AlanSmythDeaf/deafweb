import logging
import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm
from .models import Order

print(settings.STRIPE_SECRET_KEY)
logger = logging.getLogger(__name__)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Initialize Stripe with secret key
    stripe.api_key = stripe_secret_key

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.item_name = "Fixed Price Item"
                order.item_price = 50.00
                order.grand_total = 50.00

                # Create Stripe PaymentIntent
                logger.info(f"Creating PaymentIntent for order {order.id}")
                intent = stripe.PaymentIntent.create(
                    amount=5000,  # 50.00 EUR
                    currency='eur',
                    payment_method_types=['card'],
                    metadata={
                        'order_id': order.id,
                        'email': order.email,
                    }
                )

                logger.info(f"PaymentIntent created successfully: {intent.id}")
                print(f"Client Secret: {intent.client_secret}")

                # Link Stripe payment ID to order
                order.stripe_pid = intent.id
                order.save()

                return render(request, 'checkout/payment.html', {
                    'client_secret': intent.client_secret,
                    'stripe_public_key': stripe_public_key,
                    'order': order,
                })

            except stripe.error.StripeError as e:
                logger.error(f"Stripe error: {str(e)}")
                messages.error(request, f"Payment error: {str(e)}")
                return redirect('checkout')
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
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
