from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from decimal import *

TYPE = [
        (1, 'Private Company (PTY) LTD'),
        (2, 'Public Company (LTD)'),
        (3, 'Sole Proprietorship'),
        (4, 'Non-Profit Company (NPC)'),
        (5, 'Freelancer'),
        (6, 'Partnership'),
        (7, 'Personal Liability Company Inc.'),
    ]

# this is a model for a service provider.
class ServiceProvider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='service_provider', on_delete=models.CASCADE, blank=False, null=True)
    sp_type = models.SmallIntegerField(blank=False, choices=TYPE)
    name = models.CharField(max_length=300, blank=False)
    reg_num = models.CharField(max_length=35, blank=True)
    address = models.CharField(max_length=600, blank=False)
    contact_num = models.CharField(max_length=35, blank=False)
    contact_persons = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    provinces = models.ManyToManyField('leads_and_tenders.Province', blank=True)
    business_categories = models.ManyToManyField('leads_and_tenders.Category', blank=True)
    business_keywords = models.ManyToManyField('leads_and_tenders.Keywords', blank=True)
    sp_keywords = models.ManyToManyField('service_provider.SP_Keyword', blank=True)
    assigned_tenders = models.ManyToManyField('leads_and_tenders.Tender', through='leads_and_tenders.SP_Tender', blank=True)
    chosen_plan = models.ManyToManyField('pricing_plans.PricingPlan', blank=True, through='PlanSubscription')
    created_at = models.DateField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('Service Providers')
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def current_plan(self):
        try:
            # Retrieve the latest subscription from plan_history
            latest_subscription = PlanSubscription.objects.filter(sp=self).latest('start_date')
            return latest_subscription.plan
        except PlanSubscription.DoesNotExist:
            return None

    def current_plan_duration(self):
        current_plan = self.current_plan()
        if current_plan:
            subscription = PlanSubscription.objects.filter(sp=self, plan=current_plan).latest('start_date')
            return subscription.duration if subscription else None
        return None


# these are keywords that are unique to the service provider.
# that is, keyword that cannot be found in our pre-populated keyword in the Keyowrds model.   
class SP_Keyword(models.Model):
    sp_keyword = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = ('Service Provider Unique Keywords')
        ordering = ['sp_keyword', ]

    def __str__(self):
        return self.sp_keyword
    

# this is an intermidiary table between the SP and their chosen plan.
class PlanSubscription(models.Model):
    CONTRACT_STATUS = [
        (1, 'active'),
        (2, 'expired'),
        (3, 'cancelled'),
        (4, 'awaiting payment confirmation'),
    ]
    sp = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.SET_NULL, related_name='service_providers', null=True)
    plan = models.ForeignKey('pricing_plans.PricingPlan', on_delete=models.SET_NULL, related_name='sp_plans', null=True)
    start_date = models.DateField(default=timezone.now, blank=False)
    status = models.SmallIntegerField(default=1, choices=CONTRACT_STATUS)
    pymnt_ref = models.CharField(max_length=10, unique=True)
    duration = models.SmallIntegerField(default=12)

    def duration(self):
        return self.duration
    
    def ret_expiry_date(self):
        return self.start_date + relativedelta(self.duration)
    


