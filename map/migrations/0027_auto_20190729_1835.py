# Generated by Django 2.0.13 on 2019-07-29 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0026_auto_20190729_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='avg_point',
            field=models.PositiveSmallIntegerField(default=30, null=True),
        ),
    ]
