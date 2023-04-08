# Generated by Django 3.2 on 2023-04-08 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0002_auto_20230408_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='is_doctor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_patient',
            field=models.BooleanField(default=False),
        ),
    ]