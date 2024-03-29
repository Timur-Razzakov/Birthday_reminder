# Generated by Django 4.1.7 on 2023-04-05 15:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reminder_service.custom_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(max_length=100, unique=True, verbose_name='user_name')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='channel_name')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='City_name')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='company_name')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('phone_number', models.CharField(max_length=13, validators=[reminder_service.custom_validators.phone_validator], verbose_name='phone_number')),
                ('email', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.EmailValidator(message='Почта неверного формата!!')], verbose_name='email')),
                ('web_site', models.URLField(blank=True, null=True, verbose_name='url')),
                ('company_motto', models.CharField(blank=True, max_length=255, null=True, verbose_name='company_motto')),
                ('logo', models.ImageField(blank=True, upload_to='logo/', validators=[reminder_service.custom_validators.validate_photo_size], verbose_name='Логотип Компании')),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=7, verbose_name='GENDER')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='full_name')),
                ('first_name', models.CharField(max_length=100, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last_name')),
                ('father_name', models.CharField(max_length=255, verbose_name='father_name')),
                ('email', models.CharField(blank=True, max_length=200, null=True, unique=True, validators=[django.core.validators.EmailValidator(message='Почта неверного формата')], verbose_name='email')),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, validators=[reminder_service.custom_validators.phone_validator], verbose_name='phone_number')),
                ('date_of_birth', models.DateField(verbose_name='date_of_birth')),
                ('inter_passport', models.CharField(max_length=9, validators=[reminder_service.custom_validators.passport_validator], verbose_name='international passport')),
                ('passport', models.CharField(max_length=9, validators=[reminder_service.custom_validators.passport_validator], verbose_name='national passport')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('traveled', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('channel', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.channel', verbose_name='channel')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.city', verbose_name='City')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.gender', verbose_name='GENDER')),
            ],
        ),
    ]
