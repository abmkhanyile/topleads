from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from leads_and_tenders.models import Category, Tender
from pricing_plans.models import PricingPlan
from .forms import TenderSearchForm
from django.utils import timezone
from django.core.paginator import Paginator

# # handles the homepage.
class Home(View, ContextMixin):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['pricing_plans'] = PricingPlan.objects.all()
        context['search_form'] = TenderSearchForm()

        tenders = Tender.objects.filter(closingDate__gt=timezone.now())
        paginator = Paginator(tenders, 30)
        pageNum = self.request.GET.get('page')
        page_obj = paginator.get_page(pageNum)

        context['page_obj'] = page_obj
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())