# Generated by Django 4.2.2 on 2023-12-13 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_provider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovider',
            name='address',
            field=models.CharField(max_length=600),
        ),
    ]
