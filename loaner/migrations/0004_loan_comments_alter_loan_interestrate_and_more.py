# Generated by Django 4.2.2 on 2023-07-12 13:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0014_alter_shareholderinstallment_comments'),
        ('loaner', '0003_loan'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='InterestRate',
            field=models.IntegerField(default='3', verbose_name='Interest Rate'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='LoanAmount',
            field=models.IntegerField(verbose_name='Loan Amount'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='LoanGivenDate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Loan Given'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='Reference1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Reference_one', to='shareholder.shareholder', verbose_name='Reference One'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='Reference2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Reference_two', to='shareholder.shareholder', verbose_name='Reference Two'),
        ),
    ]
