# Generated by Django 4.2.6 on 2024-01-16 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_alter_callreport_collecteddtmfs_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bulkId', models.UUIDField(unique=True)),
                ('messageId', models.UUIDField()),
                ('from_number', models.CharField(max_length=20)),
                ('to', models.CharField(max_length=20)),
                ('sentAt', models.DateTimeField()),
                ('mccMnc', models.CharField(max_length=20)),
                ('callbackData', models.CharField(max_length=100)),
                ('voiceCall', models.JSONField()),
                ('price', models.JSONField()),
                ('status', models.JSONField()),
                ('error', models.JSONField()),
            ],
        ),
        migrations.DeleteModel(
            name='CallReport',
        ),
    ]
