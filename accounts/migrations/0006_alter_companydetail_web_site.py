# Generated by Django 4.1.7 on 2023-03-20 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_myuser_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetail',
            name='web_site',
            field=models.URLField(blank=True, null=True, verbose_name='url'),
        ),
    ]
