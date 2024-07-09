# Generated by Django 4.2.6 on 2024-01-16 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_rename_dtmf_codes_callreport_bulkid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callreport',
            name='collectedDtmfs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='callreport',
            name='currency',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='callreport',
            name='pricePerSecond',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='callreport',
            name='scenarioId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='callreport',
            name='scenarioName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
