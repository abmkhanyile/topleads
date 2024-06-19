# Generated by Django 4.2.2 on 2023-12-26 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pricing_plans', '0001_initial'),
        ('service_provider', '0013_rename_chosen_plan_serviceprovider_historical_plan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovider',
            name='active_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_providers', to='pricing_plans.pricingplan'),
        ),
    ]
