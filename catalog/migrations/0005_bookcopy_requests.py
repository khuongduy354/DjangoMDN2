# Generated by Django 4.2.2 on 2023-06-22 07:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0004_remove_bookcopy_available_bookcopy_availability_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookcopy",
            name="requests",
            field=models.ManyToManyField(
                related_name="requests", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]