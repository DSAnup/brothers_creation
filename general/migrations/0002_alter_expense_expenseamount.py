# Generated by Django 4.2.3 on 2023-07-30 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='ExpenseAmount',
            field=models.IntegerField(verbose_name='Expense Amount'),
        ),
    ]
