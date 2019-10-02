# Generated by Django 2.0.13 on 2019-09-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0044_auto_20190930_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='alt_name',
            field=models.TextField(blank=True, help_text='Enter list of alternative names for dish. Divider comma', null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='cooking_method',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='eng_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]