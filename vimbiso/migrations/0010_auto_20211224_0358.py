# Generated by Django 3.1.6 on 2021-12-23 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vimbiso', '0009_businessprofile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
