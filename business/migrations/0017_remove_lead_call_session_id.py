# Generated by Django 4.2.6 on 2024-05-20 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0016_rename_extras_lead_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='call_session_id',
        ),
    ]