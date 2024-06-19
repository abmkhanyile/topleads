from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Tender)
class ServiceProviderAdmin(admin.ModelAdmin):
    filter_horizontal = ('assigned_keywords', 'tenderCategory', 'tenderProvince')

admin.site.register(models.Category)
admin.site.register(models.Province)
admin.site.register(models.Keywords)
admin.site.register(models.SP_Tender)