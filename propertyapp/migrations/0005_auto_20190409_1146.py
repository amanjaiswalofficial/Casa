# Generated by Django 2.1.7 on 2019-04-09 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('propertyapp', '0004_enquiry_enquiry_person_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiry',
            name='enquiry_property',
        ),
        migrations.AddField(
            model_name='enquiry',
            name='enquiry_property',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='propertyapp.Property'),
        ),
    ]