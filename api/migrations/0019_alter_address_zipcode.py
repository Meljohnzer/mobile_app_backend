# Generated by Django 4.1.7 on 2023-04-04 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_company_user_alter_userdetails_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(max_length=12),
        ),
    ]