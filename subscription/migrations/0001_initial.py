# Generated by Django 5.0.6 on 2024-05-22 13:11

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('Basic', 'Basic'), ('Premium', 'Premium'), ('Enterprise', 'Enterprise')], default='BASIC', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_cycle', models.CharField(choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Monthly', max_length=10)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='Inactive', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
