# Generated by Django 2.0.5 on 2018-09-02 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0050_auto_20180901_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formbasic',
            name='diagnostic_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reocurring',
            name='diagnostic_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
