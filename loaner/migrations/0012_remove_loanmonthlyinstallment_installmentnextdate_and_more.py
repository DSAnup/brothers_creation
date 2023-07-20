# Generated by Django 4.2.2 on 2023-07-17 10:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('loaner', '0011_loanmonthlyinstallment_installmentnextdate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanmonthlyinstallment',
            name='InstallmentNextDate',
        ),
        migrations.AddField(
            model_name='loanmonthlyinstallment',
            name='InstallmentMonth',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Installment Month'),
        ),
        migrations.AlterField(
            model_name='loanmonthlyinstallment',
            name='InstallmentDate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Installment Paid Date'),
        ),
    ]