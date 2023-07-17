# Generated by Django 4.2.2 on 2023-07-12 13:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0014_alter_shareholderinstallment_comments'),
        ('loaner', '0002_alter_loaner_profilepic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LoanAmount', models.IntegerField()),
                ('LoanGivenDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('InterestRate', models.IntegerField(default='3')),
                ('InterestPay', models.IntegerField(blank=True, null=True)),
                ('CreatedBy', models.IntegerField(blank=True, null=True)),
                ('DateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('DateLastUpdated', models.DateTimeField(default=django.utils.timezone.now)),
                ('UpdatedBy', models.IntegerField(blank=True, null=True)),
                ('Loaner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loaner.loaner', verbose_name='Loaner')),
                ('Reference1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Reference_one', to='shareholder.shareholder')),
                ('Reference2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Reference_two', to='shareholder.shareholder')),
            ],
        ),
    ]