# Generated by Django 2.2.4 on 2019-11-12 02:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reading_count', '0005_auto_20191112_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
