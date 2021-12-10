# Generated by Django 3.1.6 on 2021-12-03 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vimbiso', '0002_user_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='media')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='businessprofile',
            name='image',
            field=models.ImageField(default=None, upload_to='media'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='is_resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reviews',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reviews',
            name='response',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ReviewResponse',
        ),
    ]