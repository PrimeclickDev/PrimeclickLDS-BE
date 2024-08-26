import uuid
from django.utils import timezone
from accounts.models import User
from cloudinary.models import CloudinaryField
from django.db import models, transaction
import random
import string
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db.models import F
from django.db.models.signals import post_delete
from django.dispatch import receiver


def generate_random_id(length=4):
    characters = string.ascii_uppercase + string.digits
    return 'B' + ''.join(random.choice(characters) for _ in range(length - 1))


def random_id(length=12):
    characters = string.ascii_uppercase + string.digits
    return 'C' + ''.join(random.choice(characters) for _ in range(length - 1))


class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    users = models.ManyToManyField(User, related_name="businesses", blank=True)
    email = models.EmailField()
    avatar = models.ImageField(
        upload_to='user_avatar/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Campaign(models.Model):
    TYPE_OF_CAMPAIGN = (
        ('UPLOAD', 'Upload'),
        ('DIRECT', 'Direct')
    )

    CONTACT_OPTION = (
        ("CALL", "Call"),
        ("SMS", "Sms")
    )

    id = models.CharField(max_length=4, primary_key=True,
                          unique=True, editable=False)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='business_campaign', to_field='id')
    title = models.CharField(max_length=255, null=True, blank=True)
    leads = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type_of = models.CharField(
        max_length=30, choices=TYPE_OF_CAMPAIGN)
    converted = models.IntegerField(default=0)
    contact_option = models.CharField(max_length=30, choices=CONTACT_OPTION)
    audio_link_1 = models.CharField(max_length=100, null=True, blank=True)
    audio_link_2 = models.CharField(max_length=100, null=True, blank=True)
    audio_link_3 = models.CharField(max_length=100, null=True, blank=True)
    audio_link_4 = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_random_id()
        super(Campaign, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lead(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Contacted', 'Contacted'),
    )

    CONTACTED_CHOICES = (
        ('Pending', 'Pending'),
        ('Converted', 'Converted'),
        ('Rejected', 'Rejected'),
    )

    id = models.CharField(max_length=12, primary_key=True, unique=True, editable=False)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='campaign_lead', to_field='id')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')
    contacted_status = models.CharField(
        max_length=20, choices=CONTACTED_CHOICES, default='Pending')
    session_id = models.CharField(max_length=100, null=True, blank=True)
    recording_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = random_id()
            while Lead.objects.filter(id=self.id).exists():
                self.id = random_id()
        super(Lead, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class CallReport(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name="call_reports_lead", to_field='id')
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="call_reports_campaign", to_field="id")
    report = models.JSONField()

    # audio_file = CloudinaryField(upload_to='user_audio/', storage=MediaCloudinaryStorage(), blank=True, null=True)

    def __str__(self):
        return self.lead.full_name


class FormDesign(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="form_design", to_field="id")
    design = models.TextField()

    def __str__(self):
        return f"{self.campaign}'s form custom design"


class ViewTimeHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="view_time")
    email = models.EmailField()
    sent_time = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=255, null=True, blank=True)
    access_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email


@receiver(post_delete, sender=Lead)
def recount_leads(sender, instance, **kwargs):
    with transaction.atomic():
        campaign = instance.campaign
        if campaign:
            campaign.leads = Lead.objects.filter(campaign=campaign).count()
            campaign.save()
