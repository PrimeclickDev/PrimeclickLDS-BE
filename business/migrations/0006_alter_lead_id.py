# Generated by Django 4.2.6 on 2024-08-26 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_lead_recording_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='id',
            field=models.CharField(editable=False, max_length=8, primary_key=True, serialize=False, unique=True),
        ),
    ]
