# Generated by Django 5.0.6 on 2024-05-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_profile_profile_picture_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
