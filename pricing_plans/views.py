from django.shortcuts import render
from pricing_plans.models import PricingPlan
from django.views.generic.base import View, ContextMixin

class PricingView(View, ContextMixin):
    template_name = "pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['pricing_plans'] = PricingPlan.objects.all()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

