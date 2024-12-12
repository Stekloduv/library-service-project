# Generated by Django 5.1.3 on 2024-12-12 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("borrowing", "0002_alter_borrowing_actual_return_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "Pending"), ("PAID", "Paid")],
                        default="PENDING",
                        max_length=7,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PAYMENT", "Payment"), ("FINE", "Fine")], max_length=7
                    ),
                ),
                ("session_url", models.URLField(blank=True, max_length=511, null=True)),
                ("session_id", models.CharField(blank=True, max_length=511, null=True)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="borrowing.borrowing",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("borrowing", "session_id"),
                        name="unique_borrowing_session_id",
                    )
                ],
            },
        ),
    ]
