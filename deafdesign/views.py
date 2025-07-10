from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NewsletterSubscriber


def subscribe_newsletter(request):
    """View to handle newsletter subscriptions."""
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email is already subscribed
        if not NewsletterSubscriber.objects.filter(email=email).exists():
            # Create a new subscription
            NewsletterSubscriber.objects.create(email=email)
            messages.success(
                request,
                'You have successfully subscribed to our newsletter.'
            )

            # Redirect to a confirmation page after successful subscription
            return render(
                request,
                'newsletter/newsletter_subscribe_success.html'
            )
        else:
            # Inform the user they are already subscribed
            messages.info(
                request,
                'You are already subscribed to our newsletter.'
            )

    # If the request method is GET or invalid POST data, redirect to home
    return redirect('home')


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)

def handler500(request):
    """ Error Handler 500 - Internal Server Error """
    return render(request, "errors/500.html", status=500)
