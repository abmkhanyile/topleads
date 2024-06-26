from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
import re

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if path == reverse('user_accounts:logout_success').lstrip('/'):
            logout(request)

        if request.user.is_authenticated and url_is_exempt:
            if path == 'user_accounts/auto_complete_search/':
                return None
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or url_is_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL)


# payment_middleware.py
class PaymentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated and has not made a payment
        if request.user.is_authenticated and not request.user.has_made_payment:  
            # Replace 'has_made_payment' with the actual condition for checking payment status
            # You may need to implement a way to check if the user has made a payment

            # Allow access to the logout view
            if request.path != reverse('logout'):  
                # Redirect to the payment page if not logged out
                return redirect('payment_page')  # Replace 'payment_page' with your payment page URL

        return response
