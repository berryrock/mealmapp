# Generated by Django 2.0.13 on 2019-08-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0032_auto_20190821_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='parsed',
            field=models.BooleanField(default=False),
        ),
    ]