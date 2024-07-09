# Generated by Django 4.2.6 on 2024-07-09 14:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0020_remove_lead_check_it'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewTimeHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('sent_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('link', models.CharField(max_length=255)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='view_time', to='business.campaign')),
            ],
        ),
    ]
