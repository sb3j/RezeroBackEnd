# Generated by Django 5.0.7 on 2024-07-10 04:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_customuser_business_registration_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="userId",
            field=models.CharField(default="", max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
