# Generated by Django 3.1.6 on 2021-12-10 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vimbiso', '0004_remove_businessprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
