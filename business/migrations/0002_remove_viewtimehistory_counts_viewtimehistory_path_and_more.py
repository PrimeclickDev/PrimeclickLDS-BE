# Generated by Django 4.2.6 on 2024-07-10 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viewtimehistory',
            name='counts',
        ),
        migrations.AddField(
            model_name='viewtimehistory',
            name='path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='viewtimehistory',
            name='link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
