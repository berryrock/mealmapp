# Generated by Django 2.0.13 on 2019-06-17 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20190617_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='main_picture',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
