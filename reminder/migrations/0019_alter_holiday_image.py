# Generated by Django 4.1.7 on 2023-03-19 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0018_alter_templateforchannel_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='holiday/%Y/%m/%d', verbose_name='Изображение'),
        ),
    ]