# Generated by Django 4.2.2 on 2023-07-16 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loaner', '0005_rename_comments_loan_comments_loan_loannumber_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='isClosed',
            field=models.BooleanField(default=False, verbose_name='Is Closed'),
        ),
    ]
