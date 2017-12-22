# Generated by Django 2.0 on 2017-12-19 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_auto_20171216_0326'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceFacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=30)),
                ('os_version', models.CharField(max_length=30)),
                ('fqdn', models.CharField(max_length=30)),
                ('serial_number', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
            ],
        ),
    ]