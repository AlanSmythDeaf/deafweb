import logging
import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm
from .models import Order

from django.template.loader import render_to_string
from django.core.mail import send_mail


print(settings.STRIPE_SECRET_KEY)
logger = logging.getLogger(__name__)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Initialize Stripe with secret key
    stripe.api_key = stripe_secret_key

    # Create a PaymentIntent on page load
    try:
        intent = stripe.PaymentIntent.create(
            amount=5000,  # 50.00 EUR
            currency='eur',
            payment_method_types=['card'],
        )
        client_secret = intent.client_secret
        logger.info(f"PaymentIntent created successfully: {intent.id}")
        print(f"Client Secret: {client_secret}")
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        messages.error(request, f"Payment error: {str(e)}")
        client_secret = None

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.item_name = "Fixed Price Item"
                order.item_price = 50.00
                order.grand_total = 50.00

                # Update the existing PaymentIntent with order details
                intent = stripe.PaymentIntent.modify(
                    intent.id,
                    metadata={
                        'order_id': order.id,
                        'email': order.email,
                    }
                )

                # Link Stripe payment ID to order
                order.stripe_pid = intent.id
                order.save()

                return redirect('checkout_success', order_id=order.id)

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
        'client_secret': client_secret,
        'fixed_price': 50.00,
    }

    return render(request, template, context)

def checkout_success(request, order_id):
    """
    Handle successful checkouts and send confirmation email
    """
    try:
        # Fetch the order using the provided order_id
        order = Order.objects.get(id=order_id)
        messages.success(request, f"Payment completed successfully for {order.full_name}.")

        # Prepare email content using your plain text template
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        ).strip()  

        message = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order}
        )
        
        recipient = order.email

        # Send confirmation email as plain text
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  
            [recipient],                  
            fail_silently=False,
        )
        logger.info(f"Order confirmation email sent to {recipient}")

    except Order.DoesNotExist:
        logger.error(f"Order with ID {order_id} does not exist.")
        messages.error(request, "Order not found.")
        return redirect('checkout')
    except Exception as e:
        logger.error(f"Error sending confirmation email: {str(e)}")
        messages.error(request, "Could not send confirmation email.")

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
