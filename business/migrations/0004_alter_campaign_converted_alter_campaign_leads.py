# Generated by Django 4.2.6 on 2023-11-08 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_alter_lead_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='converted',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='leads',
            field=models.IntegerField(default=0),
        ),
    ]
