# Generated by Django 2.0.4 on 2018-06-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algo', '0007_auto_20180503_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='pnstats',
            name='experiment_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pustats',
            name='experiment_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]