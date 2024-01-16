# Generated by Django 4.2.6 on 2023-11-07 10:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.CharField(editable=False, max_length=4, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('leads', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type_of_campaign', models.CharField(choices=[('UPLOAD', 'Upload'), ('DIRECT', 'Direct')], max_length=30)),
                ('converted', models.IntegerField()),
                ('actions', models.CharField(blank=True, max_length=50, null=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_campaign', to='business.business')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.CharField(editable=False, max_length=4, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=255)),
                ('actions', models.CharField(max_length=255)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_lead', to='business.campaign')),
            ],
        ),
    ]