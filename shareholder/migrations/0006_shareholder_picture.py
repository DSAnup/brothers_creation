# Generated by Django 4.2.2 on 2023-06-25 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0005_remove_shareholder_profilepic'),
    ]

    operations = [
        migrations.AddField(
            model_name='shareholder',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
