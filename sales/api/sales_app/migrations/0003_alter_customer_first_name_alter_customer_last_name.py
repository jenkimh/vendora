# Generated by Django 4.1.7 on 2023-09-26 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sales_app", "0002_alter_customer_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="first_name",
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="customer",
            name="last_name",
            field=models.CharField(max_length=30),
        ),
    ]
