# Generated by Django 3.2.16 on 2023-01-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0008_alter_account_background_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='background_pic',
            field=models.ImageField(blank=True, default='port-6.jpeg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to=''),
        ),
    ]
