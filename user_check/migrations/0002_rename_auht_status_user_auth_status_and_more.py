# Generated by Django 4.2.3 on 2023-09-07 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_check', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='auht_status',
            new_name='auth_status',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='auht_type',
            new_name='auth_type',
        ),
    ]
