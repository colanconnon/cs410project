# Generated by Django 2.1.3 on 2018-11-24 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videosearchengine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invertedindexlookup',
            name='tfid_value',
            field=models.FloatField(),
        ),
    ]
