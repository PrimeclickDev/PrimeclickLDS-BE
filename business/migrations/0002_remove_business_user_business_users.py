# Generated by Django 4.2.6 on 2024-07-11 18:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='user',
        ),
        migrations.AddField(
            model_name='business',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='businesses', to=settings.AUTH_USER_MODEL),
        ),
    ]
