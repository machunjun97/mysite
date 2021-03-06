# Generated by Django 2.2.4 on 2019-11-12 00:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reading_count', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadDetail',
            fields=[
                ('readnum_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reading_count.ReadNum')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            bases=('reading_count.readnum',),
        ),
    ]
