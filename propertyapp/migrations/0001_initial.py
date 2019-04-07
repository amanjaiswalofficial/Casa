# Generated by Django 2.1.7 on 2019-04-06 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_title', models.CharField(max_length=20)),
                ('property_address', models.CharField(max_length=20)),
                ('property_pin', models.IntegerField()),
                ('property_price', models.IntegerField()),
                ('property_bedroom', models.IntegerField()),
                ('property_bathroom', models.IntegerField()),
                ('property_sq_feet', models.IntegerField()),
                ('property_lot_size', models.IntegerField(default=0)),
                ('property_garage', models.IntegerField(default=0)),
                ('property_listing_date', models.DateField(auto_now_add=True)),
                ('property_description', models.CharField(max_length=200)),
                ('property_poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyposter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_image', models.ImageField(default='property/default/blank_home.jpg', upload_to='property/')),
                ('property_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyname', to='propertyapp.Property')),
            ],
        ),
    ]