# Generated by Django 4.2.3 on 2023-08-10 16:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('loaner', '0022_alter_loanmonthlyinstallment_installmentmonth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanmonthlyinstallment',
            name='InstallmentAmount',
            field=models.IntegerField(verbose_name='Interest Amount'),
        ),
        migrations.AlterField(
            model_name='loanmonthlyinstallment',
            name='InstallmentDate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Interest Paid Date'),
        ),
        migrations.AlterField(
            model_name='loanmonthlyinstallment',
            name='InstallmentMonth',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Interest Month'),
        ),
        migrations.AlterField(
            model_name='loanmonthlyinstallment',
            name='InstallmentPenalty',
            field=models.IntegerField(default='0', verbose_name='Interest Penalty Rate'),
        ),
    ]
