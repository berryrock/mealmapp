# Generated by Django 2.0.13 on 2019-08-20 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0028_auto_20190809_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='id',
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
