# Generated by Django 4.2.4 on 2023-09-18 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Logisticssite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]