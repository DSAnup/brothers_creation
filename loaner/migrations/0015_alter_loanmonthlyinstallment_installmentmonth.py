# Generated by Django 4.2.2 on 2023-07-17 10:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loaner', '0014_alter_loanmonthlyinstallment_installmentmonth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanmonthlyinstallment',
            name='InstallmentMonth',
            field=models.DateField(default=datetime.datetime(2023, 7, 1, 10, 47, 49, 55304, tzinfo=datetime.timezone.utc), verbose_name='Installment Month'),
        ),
    ]
