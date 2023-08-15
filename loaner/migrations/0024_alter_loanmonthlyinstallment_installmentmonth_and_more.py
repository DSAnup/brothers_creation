# Generated by Django 4.2.3 on 2023-07-31 16:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loaner', '0023_alter_loanmonthlyinstallment_installmentmonth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanmonthlyinstallment',
            name='InstallmentMonth',
            field=models.DateField(default=datetime.datetime(2023, 7, 1, 16, 28, 48, 293004, tzinfo=datetime.timezone.utc), verbose_name='Installment Month'),
        ),
        migrations.AlterField(
            model_name='referencebonus',
            name='PaidMonth',
            field=models.DateField(default=datetime.datetime(2023, 7, 1, 16, 28, 48, 294000, tzinfo=datetime.timezone.utc), verbose_name='Paid Month'),
        ),
    ]