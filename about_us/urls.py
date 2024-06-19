from .views import about_us_view
from django.urls import re_path

app_name = "about_us"

urlpatterns = [
    re_path(r'^$', about_us_view, name='about_us'),
]