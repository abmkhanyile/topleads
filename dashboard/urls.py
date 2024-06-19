from django.urls import path
from . import views

app_name ='dashboard'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('tender/<int:pk>/', views.TenderView.as_view(), name='tender'),
    path('tenders/', views.TendersView.as_view(), name='tenders'),
]