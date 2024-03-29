# Generated by Django 2.0.13 on 2019-08-26 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0033_auto_20190821_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TYPE', models.CharField(choices=[('DS', 'Dish'), ('PR', 'Product')], default='DS', max_length=2)),
                ('preference', models.PositiveSmallIntegerField(default=30)),
                ('frequency', models.PositiveSmallIntegerField(default=1)),
                ('weight_effect', models.PositiveSmallIntegerField(default=30)),
                ('last_meal_date', models.DateField(blank=True)),
                ('dish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.Dish')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.AppUser')),
            ],
        ),
        migrations.AlterField(
            model_name='mealhistory',
            name='weight',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
