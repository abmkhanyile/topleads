
from django.urls import re_path, path, include

from django.contrib.auth import views as auth_views
from . import views 

# from tender_details.views import tenders_list_view, send_email_view
# from contact_us.views import contact_us_view, email_success_view
# from articleApp.views import article_view, article_list_view
# from tenderwiz.views import privacy_policy_view, termsAndConditions_view

app_name = "user_accounts"

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('login/', auth_views.LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('logout_success/', views.logout_success_view, name='logout_success'),
    # re_path(r'^dashboard/', include('dashboard.urls')),
    path('register/<int:pk>/', views.Register.as_view(), name='register'),
    # re_path(r'^tenders/$', tenders_list_view, name='dashboard_tenders'),
    # re_path(r'^articles/$', article_list_view, name='dashboard_article_list'),
    # re_path(r'^article/(?P<article_pk>\d+)/$', article_view, name='article'),
    # re_path(r'^profile/$', profile_view, name='user_profile'),
    # re_path(r'^contact_us/$', contact_us_view, name='dashboard_contact_us'),
    # re_path(r'^billing/$', billing_view, name='billing'),
    # re_path(r'^invoice/(?P<inv_id>\d+)/$', Invoice_view, name='invoice'),
    path('registration_success/', views.registration_success_view, name='registration-success'),
    # re_path(r'^companyProfileEdit/(?P<pk>\d+)/$', UpdateCompanyProfile, name='company_profile_edit'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="authentication/password_change.html"), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
    path('find-keywords/', views.find_keywords, name="find-keywords")
    # re_path(r'^auto_complete_search/$', autocomplete_search_view, name='autocomplete_search'),
    # re_path(r'^send_email/$', send_email_view, name='sendEmail'),
    # re_path(r'^payment_success/$', Payment_Success_View, name='payment_success'),
    # re_path(r'^payment_cancelled/$', Payment_Cancelled_View, name='payment_cancelled'),
    # re_path(r'^termsAndConditions/$', termsAndConditions_view, name='dash_ts_and_cs'),
    # re_path(r'^privacy_policy/$', privacy_policy_view, name='dash_privacy_policy'),
    ]