from django.contrib import admin
from .models import ServiceProvider, SP_Keyword, PlanSubscription

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    # list_display = ['refNum', 'issueDate', 'closingDate', 'kw_assigned']
    # list_filter = ('kw_assigned',)
    filter_horizontal = ('business_keywords', 'provinces', 'business_categories')


admin.site.register(SP_Keyword)
admin.site.register(PlanSubscription)
