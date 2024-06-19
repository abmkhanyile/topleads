# from .utils import render_to_pdf

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import (
    CustomUserForm,
    PayFast_Form,                   
)

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
import json
from urllib.parse import urlencode, quote_plus
import hashlib
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, ContextMixin
from formtools.wizard.views import SessionWizardView
from formtools import wizard

from formtools.preview import FormPreview
from user_accounts.forms import CustomUserForm
from service_provider import forms as sp_forms
from service_provider.models import ServiceProvider, PlanSubscription
from leads_and_tenders.models import Keywords, Province, Category
from pricing_plans.models import PricingPlan
import random
import string
from invoices.models import Invoice

# this function generates an invoice number
def generate_invoice_number():
    # Get the last invoice number from the database
    last_invoice = Invoice.objects.order_by('-invoice_num').first()

    if last_invoice:
        new_invoice_number = last_invoice.invoice_num + 1
    else:
        # If no previous invoices, start with the initial invoice number
        new_invoice_number = 1000000

    return new_invoice_number

def generate_random_string():
    # Generate 4 random capital letters
    letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

    # Generate 4 random digits
    digits = ''.join(random.choice(string.digits) for _ in range(4))

    # Combine the letters and digits
    random_string = letters + digits

    # Shuffle the characters to make the order random
    random_string_list = list(random_string)
    random.shuffle(random_string_list)
    shuffled_string = ''.join(random_string_list)

    return shuffled_string


def logout_success_view(request):
    return render(request, 'user_accounts/logout_success.html')


def auth_view(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    else:
        messages.warning(request, "Sorry, that's not a valid username and password")
        return HttpResponseRedirect(reverse('user_accounts:login'))
    

# handles user registrations.
FORMS = [
    ("0", CustomUserForm),
    ("1", sp_forms.SP_Form1),
    ("2", sp_forms.SP_Form2),
    ("3", PayFast_Form),
]

TEMPLATES = {
    '0': "registration/form1.html",
    '1': "registration/form2.html",
    '2': "registration/form3.html",
}

# handles  the purchasing of Third-Party Insurance.
class Register(SessionWizardView):
    form_list = [CustomUserForm, sp_forms.SP_Form1, sp_forms.SP_Form2]
    success_pg = "order-summary"

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['chosen_plan'] = PricingPlan.objects.get(pk=self.kwargs['pk'])              
        return context
    
    def done(self, form_list, form_dict, **kwargs):
        user_form = form_dict['0']
        user = user_form.save(commit=False)
        user.username = user.email
        user.save()

        # here we create the service provider profile.
        sp_type = form_dict['2'].cleaned_data['sp_type']
        trading_name = form_dict['1'].cleaned_data['trading_name']
        regnum = form_dict['1'].cleaned_data['regnum']
        address = form_dict['1'].cleaned_data['address']
        contact_num = form_dict['1'].cleaned_data['contact_num']
        provinces = form_dict['2'].cleaned_data['provinces']
        business_categories = form_dict['2'].cleaned_data['business_categories']
        business_keywords = form_dict['2'].cleaned_data['business_keywords']
        
        sp = ServiceProvider.objects.create(
            user=user,
            sp_type=int(sp_type),
            name=trading_name,
            reg_num=regnum,
            address=address,
            contact_num=contact_num
        )
        sp.contact_persons.add(user)
        # here we add the provinces to the sp's ManyToManyField of provinces
        for province in provinces:
            sp.provinces.add(province)
        
        for category in business_categories:
            sp.business_categories.add(category)

        biz_keyword = business_keywords.strip("[]").split(",")

        for keyword in biz_keyword:
            kw = keyword.strip('""').strip().strip("''")
            try:
                sp.business_keywords.add(Keywords.objects.get(pk=int(kw)))
            except Keywords.DoesNotExist:
                pass

        context = self.get_context_data(form=form_list[2])

        plan_subscription = PlanSubscription.objects.create(
            sp=sp, 
            plan=context['chosen_plan'], 
            status=4,
            pymnt_ref=generate_random_string()
        )
        
        invoice = Invoice.objects.create(
            sp=sp,
            invoice_num=generate_invoice_number(),
            plan=plan_subscription
        )

        return render(self.request, 'registration/registration_success.html', {
            'user': user,
            'sp': sp,
            'subscription': plan_subscription,
            'invoice': invoice
        })


# this view processing a payment through a PayFast gateway.
def process_payment(request):
    if request.method == 'POST':
        invoice = Invoice.objects.get(pk=inv_num)
        compProfile = invoice.company
        userObj = compProfile.user

        ourDetails = OurDetails.objects.get(compRegNum='2017/417565/07')

        amount = None

        if compProfile.contractDuration == 6:
            amount = compProfile.package.sixMonthPrice
        else:
            amount = compProfile.package.annualPrice

        payfast_data = {

        }

        signature = ''
        # for key, value in payfast_data.items():
        #     signature += '{}={}&'.format(str(key), str(urllib.parse.urlencode(value)))

        signature = urlencode(payfast_data, quote_via=quote_plus)

        signature = hashlib.md5(signature.encode()).hexdigest()

        payfast_data.update({'signature': signature})

        payfastForm = PayFast_Form(payfast_data)

        context = {
            'invoice': invoice,
            'user': userObj,
            'comp_prof': compProfile,
            'ourDetails': ourDetails,
            'payfast_form': payfastForm,
            'signature': signature.strip()
        }

        return render(request, 'invoice.html', context)


@login_required
def profile_view(request):
    pass



def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_accounts/profile')
        else:
            return redirect('/user_accounts/password_change')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'user_accounts/password_change.html', args)


#Password reset view
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_accounts/profile')
        else:
            return redirect('/user_accounts/password_change')
    else:
        form = PasswordResetForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'user_accounts/password_change.html', args)

#This is the function that handle the auto complete search functionality.
def autocomplete_search_view(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
        return HttpResponse([{}], content_type='application/json')

    swList = search_text.split()

    keywords = []
    if len(swList) == 1:
        keywords = Keywords.objects.filter(keyword__icontains=swList[0].strip())
    else:
        keywords = Keywords.objects.filter(keyword__icontains=swList[0].strip()).filter(keyword__icontains=swList[1].strip())

    data = serializers.serialize('json', keywords, fields=('keyword'))
    return HttpResponse(data, content_type='application/json')


# this view handles the update of the Company Profile.
def UpdateCompanyProfile(request, pk):
    pass
    # compObj = get_object_or_404(CompanyProfile, pk=pk)

    # if request.user == compObj.user:
    #     if request.method == 'POST':
    #         companyProfileEditFormObj = CompanyProfileEditForm(data=request.POST, instance=compObj)
    #         if companyProfileEditFormObj.is_valid():
    #             editedCompObj = companyProfileEditFormObj.save()

    #             keyword_ids_str = companyProfileEditFormObj.cleaned_data['keywordListItem']

    #             if len(keyword_ids_str) > 0:
    #                 keyword_ids = keyword_ids_str.split(',')
    #                 editedCompObj.keywords.clear()
    #                 for keyword_id in keyword_ids:
    #                     keywordObj = Keywords.objects.get(id=int(keyword_id.strip()))
    #                     editedCompObj.keywords.add(keywordObj)     #adds keywords to the relationship

    #         else:
    #             print('evaluated false...')

    #         return HttpResponseRedirect('/user_accounts/profile')
    #     else:
    #         companyProfileEditFormObj = CompanyProfileEditForm(instance=compObj)
    #         return render(request, 'companyProfileEdit.html', {'compForm': companyProfileEditFormObj, 'compProf': compObj})
    # else:
    #     raise Http404("Company does not exist")


# this view displays the success page after the user finishes the registration process.
def registration_success_view(request):
    username = request.user.username
    password = request.user.password
    user = auth.authenticate(username=username, password=password)

    auth.login(request, user)
    return HttpResponseRedirect(reverse('user_accounts:registration-success'))


def Payment_Success_View(request):
    return render(request, 'payment_success.html')

def Payment_Cancelled_View(request):
    return render(request, 'payment_cancelled.html')



# this handles the pdf render.
def Invoice_view(request, inv_id):
    pass



# billing view displays all the invoices
@login_required
def billing_view(request):
    pass
    # comp = CompanyProfile.objects.get(pk=request.user.id)
    # invoices = Invoices.objects.filter(company=comp)
    # return render(request, 'billing.html', {'invoices': invoices})


# handles user registration and service provider.
class UserRegistraionFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        return HttpResponseRedirect('/form/success')


#This is the function that handle the auto complete search functionality.
def find_keywords(request):
    # if request.method == 'POST':
    #     search_text = request.POST['search_text']
    # else:
    #     search_text = ''
    #     return HttpResponse([{}], content_type='application/json')

    # swList = search_text.split()

    # print(swList)

    # keywords = []
    # if len(swList) == 1:
    #     keywords = Keywords.objects.filter(keyword__icontains=swList[0].strip())
    # else:
    #     keywords = Keywords.objects.filter(keyword__icontains=swList[0].strip()).filter(keyword__icontains=swList[1].strip())

    # data = serializers.serialize('json', keywords, fields=('keyword'))
    # return HttpResponse(data, content_type='application/json')

    search_text = request.POST.get('search_text', '')

    if len(search_text) >= 3:
        # Use case-insensitive search for keywords
        matching_keywords = Keywords.objects.filter(keyword__icontains=search_text)  # Limiting to 10 results

        # Prepare data to be sent as JSON
        data = [{'pk': keyword.pk, 'fields': {'keyword': keyword.keyword}} for keyword in matching_keywords]
        return JsonResponse(data, safe=False)
    else:
        # If the search term is less than 3 characters, return an empty list
        return JsonResponse([], safe=False)