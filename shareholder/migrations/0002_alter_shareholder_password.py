# Generated by Django 4.2.2 on 2023-06-24 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareholder',
            name='password',
            field=models.CharField(blank=True, default='123456', max_length=100, null=True),
        ),
    ]
