# Generated by Django 2.0.4 on 2019-03-31 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algo', '0012_auto_20190331_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='pnstats',
            name='sampling_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pustats',
            name='sampling_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]