# Generated by Django 4.2.6 on 2023-10-31 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_name_user_first_name_user_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='business_name',
            field=models.CharField(default='PrimeClick', max_length=255),
            preserve_default=False,
        ),
    ]
