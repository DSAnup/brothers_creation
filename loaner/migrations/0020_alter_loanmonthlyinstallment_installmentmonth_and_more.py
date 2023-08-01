# Generated by Django 4.2.3 on 2023-08-01 03:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("loaner", "0019_alter_loanmonthlyinstallment_installmentmonth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loanmonthlyinstallment",
            name="InstallmentMonth",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 8, 1, 3, 14, 9, 283280, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Installment Month",
            ),
        ),
        migrations.AlterField(
            model_name="referencebonus",
            name="PaidMonth",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 8, 1, 3, 14, 9, 284277, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Paid Month",
            ),
        ),
    ]
