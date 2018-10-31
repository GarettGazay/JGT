# Generated by Django 2.0.5 on 2018-08-17 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0029_auto_20180814_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reocurring',
            name='month',
        ),
        migrations.AddField(
            model_name='reocurring',
            name='end_date_five',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='end_date_four',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='end_date_one',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='end_date_three',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='end_date_two',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='start_date_five',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='start_date_four',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='start_date_one',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='start_date_three',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reocurring',
            name='start_date_two',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
