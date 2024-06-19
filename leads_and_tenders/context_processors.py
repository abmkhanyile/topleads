from leads_and_tenders.models import Tender
from leads_and_tenders.models import Category, Tender
from pricing_plans.models import PricingPlan
from homepage.forms import TenderSearchForm
from django.utils import timezone
from django.core.paginator import Paginator


def retrieve_tenders(request):
    context = {}
    context['categories'] = Category.objects.all()
    context['pricing_plans'] = PricingPlan.objects.all()
    context['search_form'] = TenderSearchForm()
    
    tenders = Tender.objects.filter(closingDate__gt=timezone.now())
    paginator = Paginator(tenders, 30)
    pageNum = request.GET.get('page')
    page_obj = paginator.get_page(pageNum)

    context['page_obj'] = page_obj
  
    return context