# Generated by Django 5.1.3 on 2024-12-06 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0002_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Borrowing",
        ),
    ]