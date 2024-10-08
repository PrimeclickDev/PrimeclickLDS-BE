# Generated by Django 4.2.6 on 2024-10-08 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0008_lead_call_duration_lead_call_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('CREATION', 'CREATION'), ('MODIFICATION', 'MODIFICATION'), ('LAUNCH', 'LAUNCH')], default='CREATION', max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activitylog', to='business.business')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='campaign_activity', to='business.campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
