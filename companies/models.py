from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings

# holds the information of all the registered companies.
class Company(models.Model):
    name = models.CharField(max_length=300, blank=False)
    reg_num = models.CharField(max_length=35, blank=True)
    address = RichTextField(blank=False)
    contact_num = models.CharField(max_length=35, blank=False)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    provinces = models.ManyToManyField('leads_and_tenders.Province', blank=True)
    categories = models.ManyToManyField('leads_and_tenders.Category', blank=True)
    keywords = models.ManyToManyField('leads_and_tenders.Keywords', blank=True)

    class Meta:
        verbose_name_plural = ('Registered Companies')
        ordering = ['name']

    def __str__(self):
        return self.name

