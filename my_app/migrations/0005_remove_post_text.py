# Generated by Django 3.2.16 on 2023-01-18 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
    ]
