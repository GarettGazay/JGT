# Generated by Django 2.1.1 on 2018-09-28 03:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_convertedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='convertedfile',
            name='upload_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
