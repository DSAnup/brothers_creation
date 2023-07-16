# Generated by Django 4.2.2 on 2023-07-16 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0014_alter_shareholderinstallment_comments'),
        ('loaner', '0006_loan_isclosed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loan',
            options={'get_latest_by': 'LoanNumber'},
        ),
        migrations.AlterField(
            model_name='loan',
            name='LoanNumber',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='loan',
            name='Reference1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Reference_one', to='shareholder.shareholder', verbose_name='Reference One'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='Reference2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Reference_two', to='shareholder.shareholder', verbose_name='Reference Two'),
        ),
    ]
