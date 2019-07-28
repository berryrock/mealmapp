# Generated by Django 2.0.13 on 2019-07-26 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0018_auto_20190709_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('borders', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='appuser',
            name='region',
            field=models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='map.Region'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='region',
            field=models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='map.Region'),
        ),
        migrations.AlterField(
            model_name='regionvector',
            name='region',
            field=models.ForeignKey(blank=True, db_index=False, default='russia', null=True, on_delete=django.db.models.deletion.SET_NULL, to='map.Region'),
        ),
    ]
