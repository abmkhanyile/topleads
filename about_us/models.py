from django.db import models
from ckeditor.fields import RichTextField

class AboutUsInfo(models.Model):
    about = RichTextField(blank=False)

    class Meta:
        verbose_name_plural = ('About Us Page')
