from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from checkout.models import Order 


class StripeWH_Handler:
    """Handle Stripe webhooks"""
    def webhooks(request):
        print("Stripe webhook endpoint called!")

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        print(f"Preparing to send email to {order.email}")
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        print(f"Email subject: {subject}")
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        print(f"Email body: {body}")

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email]
        )
        print("send_mail called")

    def handle_event(self, event):
        print(f"Unhandled event received: {event['type']}")
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        print("Webhook: payment_intent.succeeded received")
        intent = event['data']['object']
        stripe_pid = intent['id']
        print(f"Stripe PID from webhook: {stripe_pid}")

        try:
            order = Order.objects.get(stripe_pid=stripe_pid)
            print(f"Order found: {order.id}, email: {order.email}")
            self._send_confirmation_email(order)
        except Order.DoesNotExist:
            print(f"Order with stripe_pid {stripe_pid} not found.")

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        print("Webhook: payment_intent.payment_failed received")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
