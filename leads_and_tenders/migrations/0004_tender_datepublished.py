# Generated by Django 4.2.2 on 2023-11-09 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads_and_tenders', '0003_rename_siteinspection_tender_siteinspectionaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='datePublished',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
