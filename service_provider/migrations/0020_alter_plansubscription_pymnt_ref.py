# Generated by Django 4.2.2 on 2023-12-30 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_provider', '0019_alter_plansubscription_plan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plansubscription',
            name='pymnt_ref',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]