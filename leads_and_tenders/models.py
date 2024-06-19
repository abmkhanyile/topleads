from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone


#Stores the categories.
class Category(models.Model):
    catDescription = models.CharField(max_length=100)
    cat_icon = models.ImageField(upload_to='category_icons/', blank=True)

    @property
    def get_num_of_assigned_tender(self):
        return self.tender_set.all().count()

    class Meta:
        verbose_name_plural = ('Categories')

    def __str__(self):
        return self.catDescription
    
    def retcat_icon(self):
        return f"https://saleads.s3.eu-west-2.amazonaws.com/{self.cat_icon}" 


#The provinces model stores the Provinces
class Province(models.Model):
    province_name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.province_name



# This models stores the keywords in the database.
class Keywords(models.Model):
    keyword = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = ('Keywords')
        ordering = ['keyword', ]

    def __str__(self):
        return self.keyword



# #This is the model that stores the tender.
class Tender(models.Model):
    tenderCategory = models.ManyToManyField(Category, blank=False)       #this field holds the tender category, e.g. construction, engineering, human resources etc.
    tenderProvince = models.ManyToManyField(Province, blank=False)       #this is the province the tender was advertised from.
    buyersName = models.CharField(max_length=100, blank=True, null=True)   #this is the name of the Buyer e.g. Dept. of Transport, Transnet, Dept of Agriculture etc.
    summary = models.TextField(blank=False)      #this is the tender title as per the Buyer.
    refNum = models.CharField(max_length=100)    #tender ref number as per the Buyer.
    issueDate = models.DateTimeField(blank=True, null=True)     #date the tender was published
    datePublished = models.DateTimeField(blank=True, null=True)   #tender publish date
    closingDate = models.DateTimeField(default=timezone.now, blank=True, null=True)   #tender closing date
    siteInspectionDate = models.DateTimeField(blank=True, null=True)
    siteInspectionAddress = RichTextField(blank=True, null=True)     #site inspection date, if any
    enquiries = RichTextField(blank=True, null=True) #this field stores details of the contact person, for the tender.
    description = RichTextField(blank=True, null=True)   #this is the body of the tender. the tender details are captured here.
    assigned_keywords = models.ManyToManyField(Keywords, blank=True)
    tender_docs = RichTextField(blank=True)
    created_at = models.DateField(default=timezone.now, blank=False, null=False)

    class Meta:
        ordering = ['-closingDate']

    def __str__(self) -> str:
        return self.summary

    def check_if_expired(self):
        if self.closingDate != None:
            if self.closingDate < timezone.now():
                return True
            else:
                return False
        else:
            return False


# this is a bridge table for a SP and Tenders relationship
class SP_Tender(models.Model):
    service_provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.CASCADE)
    tender = models.ForeignKey('leads_and_tenders.Tender', on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now, blank=False)






