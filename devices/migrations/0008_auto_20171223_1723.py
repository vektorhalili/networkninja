# Generated by Django 2.0 on 2017-12-23 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_auto_20171223_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='id',
        ),
        migrations.AlterField(
            model_name='client',
            name='mac',
            field=models.CharField(max_length=19, primary_key=True, serialize=False),
        ),
    ]