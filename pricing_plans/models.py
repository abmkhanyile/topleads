from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

# holds all the pricing plans
class PricingPlan(models.Model):
    name = models.CharField(max_length=20, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    benefits = RichTextField()
    provinces_num = models.SmallIntegerField(blank=False, null=True)
    display_order = models.SmallIntegerField(blank=False, null=True)
    date_created = models.DateTimeField(default=timezone.now, blank=False)

    class Meta:
        verbose_name_plural = ('Pricing Plans')
        ordering = ['display_order']

    def __str__(self):
        return self.name

