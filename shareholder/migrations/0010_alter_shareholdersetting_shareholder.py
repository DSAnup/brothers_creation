# Generated by Django 4.2.2 on 2023-06-25 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0009_alter_shareholdersetting_shareholder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareholdersetting',
            name='shareHolder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shareholder.shareholder', verbose_name='Share Holder'),
        ),
    ]