from django.shortcuts import render
from .models import AboutUsInfo

def about_us_view(request):
    about_info = AboutUsInfo.objects.all()[0]
    return render(request, 'about_us.html', {'about': about_info})
