# Generated by Django 2.0.13 on 2019-08-26 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0037_auto_20190826_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.Product'),
        ),
    ]