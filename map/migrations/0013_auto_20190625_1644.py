# Generated by Django 2.0.13 on 2019-06-25 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0012_auto_20190625_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealhistory',
            name='user',
            field=models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]