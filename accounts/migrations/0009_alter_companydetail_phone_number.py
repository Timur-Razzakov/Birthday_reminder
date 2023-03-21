# Generated by Django 4.1.7 on 2023-03-20 18:11

from django.db import migrations, models
import reminder_service.custom_validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_companydetail_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetail',
            name='phone_number',
            field=models.CharField(max_length=14, validators=[reminder_service.custom_validators.phone_validator], verbose_name='phone_number'),
        ),
    ]
