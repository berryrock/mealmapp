# Generated by Django 2.0.13 on 2019-07-28 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0021_auto_20190728_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='tags',
        ),
    ]