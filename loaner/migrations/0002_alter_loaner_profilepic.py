# Generated by Django 4.2.2 on 2023-07-07 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loaner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaner',
            name='profilePic',
            field=models.FileField(blank=True, null=True, upload_to='images/loaner/'),
        ),
    ]
