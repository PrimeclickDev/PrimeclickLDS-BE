# Generated by Django 4.2.6 on 2024-08-26 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_alter_lead_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='id',
            field=models.CharField(editable=False, max_length=12, primary_key=True, serialize=False, unique=True),
        ),
    ]