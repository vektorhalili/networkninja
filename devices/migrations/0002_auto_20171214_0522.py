# Generated by Django 2.0 on 2017-12-14 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='type',
            field=models.CharField(max_length=3),
        ),
    ]
