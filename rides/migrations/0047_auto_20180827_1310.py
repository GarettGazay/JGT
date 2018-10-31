# Generated by Django 2.0.5 on 2018-08-27 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0046_auto_20180825_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formbasic',
            name='account_number',
            field=models.CharField(choices=[('SC00001', 'SC00001'), ('Fatima001', 'Fatima001'), ('OLISCC', 'OLISCC'), ('KINSCC', 'KINSCC'), ('VICSCC', 'VICSCC'), ('MCDSCC', 'MCDSCC')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='formbasic',
            name='service_type',
            field=models.CharField(choices=[('SCFHP Basic', 'SCFHP Basic'), ('VMC Wheelchair', 'VMC Wheelchair'), ('VMC Ambulatory', 'VMC Ambulatory'), ('VMC Discharge', 'VMC Discharge')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='account_number',
            field=models.CharField(choices=[('SC00001', 'SC00001'), ('Fatima001', 'Fatima001'), ('OLISCC', 'OLISCC'), ('KINSCC', 'KINSCC'), ('VICSCC', 'VICSCC'), ('MCDSCC', 'MCDSCC')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='return_time',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='service_type',
            field=models.CharField(choices=[('SCFHP Basic', 'SCFHP Basic'), ('VMC Wheelchair', 'VMC Wheelchair'), ('VMC Ambulatory', 'VMC Ambulatory'), ('VMC Discharge', 'VMC Discharge')], default='', max_length=15),
        ),
    ]
