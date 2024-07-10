# Generated by Django 5.0.7 on 2024-07-10 04:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_customuser_userid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="userId",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
