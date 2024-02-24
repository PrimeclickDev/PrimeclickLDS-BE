# Generated by Django 4.2.6 on 2024-02-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0013_lead_contacted_status_alter_lead_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callreport',
            name='answer_time',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='bulk_id',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='call_back_data',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='charged_duration',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='dtmf_codes',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='error_description',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='error_group_id',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='error_group_name',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='error_id',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='error_name',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='error_permanent',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='file_duration',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='from_number',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='group_name',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='mcc_mnc',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='message_id',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='scenario_id',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='scenario_name',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='sent_at',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='status_description',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='status_id',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='status_name',
        ),
        migrations.RemoveField(
            model_name='callreport',
            name='to_number',
        ),
        migrations.AddField(
            model_name='callreport',
            name='report',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
