# Generated by Django 4.1.7 on 2023-04-06 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0009_mailingcommerceoffer_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailingcommerceoffer',
            old_name='media',
            new_name='image',
        ),
    ]
