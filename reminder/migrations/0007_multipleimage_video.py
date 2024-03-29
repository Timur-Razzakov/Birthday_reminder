# Generated by Django 4.1.7 on 2023-04-06 12:35

from django.db import migrations, models
import reminder_service.custom_validators


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0006_remove_multipleimage_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='multipleimage',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='video/', validators=[reminder_service.custom_validators.validate_video_extension], verbose_name=' Видео'),
        ),
    ]
