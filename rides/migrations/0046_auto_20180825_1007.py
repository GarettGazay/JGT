# Generated by Django 2.0.5 on 2018-08-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0045_auto_20180824_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formbasic',
            name='account_number',
            field=models.CharField(choices=[('SC00001', 'SC00001'), ('I do not have one', 'I do not have one')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='formbasic',
            name='number_of_passengers',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='formbasic',
            name='return_time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='formbasic',
            name='service_type',
            field=models.CharField(choices=[('SCFHP Basic', 'SCFHP Basic'), ('VMC Basic', 'VMC Basic')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='account_number',
            field=models.CharField(choices=[('SC00001', 'SC00001'), ('I do not have one', 'I do not have one')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='number_of_passengers',
            field=models.PositiveIntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='return_time',
            field=models.CharField(blank=True, default='', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='service_type',
            field=models.CharField(choices=[('SCFHP Basic', 'SCFHP Basic'), ('VMC Basic', 'VMC Basic')], default='', max_length=15),
        ),
    ]