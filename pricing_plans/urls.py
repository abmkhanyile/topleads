from django.urls import path
from .views import (
    PricingView
)

app_name = 'pricing_plans'

urlpatterns = [
    path('', PricingView.as_view(), name='pricing'),
]