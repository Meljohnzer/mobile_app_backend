# Generated by Django 4.1.7 on 2023-04-09 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_apply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='zipcode',
            field=models.CharField(max_length=50),
        ),
    ]