# Generated by Django 3.2.19 on 2024-02-27 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20240227_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pressurepoint',
            name='Cpressure',
            field=models.CharField(max_length=255, null=True),
        ),
    ]