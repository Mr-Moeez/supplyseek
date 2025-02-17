# Generated by Django 5.0.6 on 2024-06-12 16:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('broadcasting', '0002_broadcast_currency_alter_broadcast_category_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(choices=[('Electronics', 'Electronics'), ('Arcade Equipment', 'Arcade Equipment'), ('Audio', 'Audio'), ('Circuit Boards & Components', 'Circuit Boards & Components'), ('Communications', 'Communications'), ('Components', 'Components'), ('Computers', 'Computers'), ('Electronics Accessories', 'Electronics Accessories'), ('GPS Accessories', 'GPS Accessories')], max_length=100)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('min_quantity', models.PositiveIntegerField(default=1)),
                ('max_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('min_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(choices=[('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('AED', 'AED'), ('HKD', 'HKD')], default='EUR', max_length=3)),
                ('type', models.CharField(choices=[('WTS', 'WTS'), ('WTB', 'WTB'), ('ALL', 'ALL')], default='ALL', max_length=3)),
                ('condition', models.CharField(choices=[('NEW', 'NEW'), ('USED', 'USED'), ('ALL', 'ALL')], default='ALL', max_length=4)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('frequency', models.CharField(choices=[('ASAP', 'ASAP'), ('DAILY', 'DAILY'), ('WEEKLY', 'WEEKLY'), ('MONTHLY', 'MONTHLY')], default='ASAP', max_length=7)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('notification_channel', models.CharField(default='email', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AlertResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_matched', models.DateTimeField(auto_now_add=True)),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alerts.alert')),
                ('broadcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='broadcasting.broadcast')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='alert',
            index=models.Index(fields=['user', 'category'], name='alerts_aler_user_id_9e5fe4_idx'),
        ),
        migrations.AddConstraint(
            model_name='alert',
            constraint=models.UniqueConstraint(fields=('user', 'search', 'category', 'country', 'brand', 'min_quantity', 'max_quantity', 'min_price', 'max_price', 'type', 'condition', 'name'), name='unique_alert'),
        ),
    ]
