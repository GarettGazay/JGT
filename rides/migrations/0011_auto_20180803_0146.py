# Generated by Django 2.0.5 on 2018-08-03 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0010_auto_20180803_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formbasic',
            name='appointment_date',
            field=models.CharField(max_length=8),
        ),
    ]