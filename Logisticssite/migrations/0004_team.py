# Generated by Django 4.2.4 on 2023-09-19 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Logisticssite', '0003_post_decs_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to='team-img')),
                ('position', models.CharField(max_length=100)),
            ],
        ),
    ]
