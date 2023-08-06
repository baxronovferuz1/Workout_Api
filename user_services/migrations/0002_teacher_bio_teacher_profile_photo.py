# Generated by Django 4.2.3 on 2023-08-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]