# Generated by Django 5.0.6 on 2024-06-21 12:27

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_logo',
            field=cloudinary.models.CloudinaryField(default=' ', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]
