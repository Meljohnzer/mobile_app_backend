# Generated by Django 4.1.7 on 2023-04-05 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_address_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
    ]
