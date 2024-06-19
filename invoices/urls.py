from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path('<pk>/', views.process_invoice_payment, name='pay-now'),
]