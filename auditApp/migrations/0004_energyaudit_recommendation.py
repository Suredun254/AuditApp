# Generated by Django 4.2.7 on 2023-11-27 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auditApp", "0003_alter_energyaudit_devices"),
    ]

    operations = [
        migrations.AddField(
            model_name="energyaudit",
            name="recommendation",
            field=models.CharField(default="", max_length=700),
        ),
    ]
