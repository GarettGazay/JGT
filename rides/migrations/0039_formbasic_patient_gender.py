# Generated by Django 2.0.5 on 2018-08-21 21:38

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0038_reocurring_patient_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='formbasic',
            name='patient_gender',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=11, null=True),
        ),
    ]
