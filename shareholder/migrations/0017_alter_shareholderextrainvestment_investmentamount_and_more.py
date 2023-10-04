# Generated by Django 4.2.5 on 2023-10-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0016_shareholderextrainvestment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareholderextrainvestment',
            name='InvestmentAmount',
            field=models.IntegerField(default=500),
        ),
        migrations.AlterField(
            model_name='shareholderextrainvestment',
            name='InvestmentNote',
            field=models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='Investment Note'),
        ),
    ]
