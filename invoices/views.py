from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Invoice
from django.conf import settings
from urllib.parse import urlencode, quote_plus
import hashlib
from requests.exceptions import RequestException



@csrf_exempt
def process_invoice_payment(request, pk):
    # retrieve invoice in question.
    invoice = Invoice.objects.get(pk=pk)

    # Use payment gateway credentials securely on the server-side

    payfast_data = {
        'merchant_id': settings.MERCHANT_ID,
        'merchant_key': settings.MERCHANT_KEY,
        'return_url': 'https://tenderpros.herokuapp.com/user_accounts/payment_success/',
        'cancel_url': 'https://tenderpros.herokuapp.com/user_accounts/payment_cancelled/',
        'name_first': invoice.sp.user.first_name,
        'name_last': invoice.sp.user.last_name,
        'email_address': invoice.sp.user.email,
        'cell_number': invoice.sp.user.contactNumber,
        'm_payment_id': invoice.invoice_num,
        'amount': invoice.plan.plan.price,
        'item_name': invoice.plan.plan.name,
        'email_confirmation': '1',
        'confirmation_address': 'ayatech.co@gmail.com'
    }

    signature = ''
        # for key, value in payfast_data.items():
        #     signature += '{}={}&'.format(str(key), str(urllib.parse.urlencode(value)))

    signature = urlencode(payfast_data, quote_via=quote_plus)

    signature = hashlib.md5(signature.encode()).hexdigest()

    payfast_data.update({'signature': signature})

    try:
        # Process payment using payment gateway API
        # Replace this with your payment gateway API integration code
        response = requests.post(
            'https://www.payfast.co.za/eng/process',
            data = payfast_data
        )

        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        # Try to decode the JSON response
        result = response.json()

        # Handle the payment response
        if result.get('success'):
            return HttpResponseRedirect('')
        else:
            return JsonResponse({'message': 'Payment failed'})

    except RequestException as e:
        return JsonResponse({'message': f'Error processing payment: {str(e)}'}, status=500)

    



