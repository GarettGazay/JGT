# Generated by Django 2.0.5 on 2018-08-03 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0009_auto_20180802_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formbasic',
            name='appointment_date',
            field=models.DateTimeField(),
        ),
    ]
