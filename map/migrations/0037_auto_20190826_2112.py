# Generated by Django 2.0.13 on 2019-08-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0036_auto_20190826_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='product',
            field=models.CharField(default=30, max_length=200),
        ),
    ]
