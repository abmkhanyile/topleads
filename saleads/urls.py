"""
URL configuration for saleads project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

app_name = 'saleads'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls', namespace='homepage')),
    path('user-accounts/', include('user_accounts.urls', namespace='user_accounts')),
    path('pricing-plans/', include('pricing_plans.urls', namespace='pricing_plans')),
    path('leads-and-tenders/', include('leads_and_tenders.urls', namespace='leads_and_tenders')),
    path('about-us/', include('about_us.urls', namespace='about_us')),
    path('contact-us/', include('contact_us.urls', namespace='contact_us')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('companies/', include('companies.urls', namespace='companies')),
    path('service-provider/', include('service_provider.urls', namespace='service_provider')),
    path('invoices/', include('invoices.urls', namespace='invoices')),
]
