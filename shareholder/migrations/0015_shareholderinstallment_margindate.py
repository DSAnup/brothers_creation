# Generated by Django 4.2.3 on 2023-08-23 03:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0014_alter_shareholderinstallment_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='shareholderinstallment',
            name='MarginDate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Margin Date'),
        ),
    ]
