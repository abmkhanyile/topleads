from django.db import models
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from decimal import *


class Invoice(models.Model):
    sp = models.ForeignKey('service_provider.ServiceProvider', related_name='sp_invoices', on_delete=models.CASCADE, blank=False)
    invoice_num = models.CharField(max_length=12, blank=False, unique=True)
    invoice_date = models.DateTimeField(default=timezone.now, blank=False)
    vat_percentage = models.IntegerField(default=15, blank=True)
    plan = models.ForeignKey('service_provider.PlanSubscription', blank=True, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False, blank=False)
    notes = models.CharField(max_length=500, blank=True, null=True)

    def total(self):
        tot = Decimal(0.00).quantize(Decimal('0.00'))
        tot = Decimal(tot + self.plan.price * self.plan.duration).quantize(Decimal('0.00'))
        return tot

    def due_date(self):
        return self.invoice_date + timedelta(days=7)

    class Meta:
        verbose_name_plural = ('Invoices')
