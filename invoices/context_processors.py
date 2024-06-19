from invoices.models import Invoice
from service_provider.models import PlanSubscription
from user_accounts.forms import PayFast_Form
from urllib.parse import urlencode, quote_plus
import hashlib


def unpaid_invoice(request):
    context = {}
    # plan = PlanSubscription.objects.filter(status=4).latest('start_date') 
    # invoice = None
    # if plan is not None:
    #     invoice = Invoice.objects.filter(plan=plan, paid=False)[0] 
    # context['global_invoice'] = invoice

    return context