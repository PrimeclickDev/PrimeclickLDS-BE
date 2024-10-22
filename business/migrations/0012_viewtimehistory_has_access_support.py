# Generated by Django 4.2.6 on 2024-10-22 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0011_merge_20241021_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewtimehistory',
            name='has_access',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('subject', models.CharField(blank=True, max_length=355, null=True)),
                ('links', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('resolved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_support', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
