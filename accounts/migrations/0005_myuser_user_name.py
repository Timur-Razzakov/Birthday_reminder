# Generated by Django 4.1.7 on 2023-03-15 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_client_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='user_name',
            field=models.CharField(default='user', max_length=100, unique=True, verbose_name='user_name'),
            preserve_default=False,
        ),
    ]
