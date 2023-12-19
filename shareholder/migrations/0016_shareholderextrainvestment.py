# Generated by Django 4.2.5 on 2023-10-04 10:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0015_shareholderinstallment_margindate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareHolderExtraInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InvestmentDate', models.DateField(default=django.utils.timezone.now, verbose_name='Investment Date')),
                ('InvestmentAmount', models.IntegerField()),
                ('InvestmentNote', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('CreatedBy', models.IntegerField(blank=True, null=True)),
                ('DateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('DateLastUpdated', models.DateTimeField(default=django.utils.timezone.now)),
                ('UpdatedBy', models.IntegerField(blank=True, null=True)),
                ('ShareHolder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shareholder.shareholder')),
            ],
        ),
    ]