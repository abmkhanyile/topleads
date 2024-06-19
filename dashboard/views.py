from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from homepage.forms import TenderSearchForm
from leads_and_tenders.models import Tender, SP_Tender

class Dashboard(View, ContextMixin):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TenderSearchForm()
        sp = SP_Tender.objects.filter(service_provider=self.request.user.service_provider)
        context['matched_tenders'] = sp
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# displays all the current tenders.
class TendersView(View, ContextMixin):
    template_name = 'tenders/tenders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
# displays a tender.
class TenderView(View, ContextMixin):
    template_name = 'tenders/tender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tender'] = Tender.objects.get(pk=self.kwargs['pk'])
        return context
    
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())