# Generated by Django 2.1.7 on 2019-04-04 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registerapp', '0006_newuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='email_field',
            field=models.EmailField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='profile_image',
            field=models.ImageField(default='register_app/blank_face.png', upload_to='user_images/'),
        ),
    ]