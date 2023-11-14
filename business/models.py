import uuid
from django.db import models
import random
import string


def generate_random_id(length=4):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Campaign(models.Model):

    TYPE_OF_CAMPAIGN = (
        ('UPLOAD', 'Upload'),
        ('DIRECT', 'Direct')
    )

    id = models.CharField(max_length=4, primary_key=True,
                          unique=True, editable=False)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='business_campaign', to_field='id')
    title = models.CharField(max_length=255)
    leads = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=30, choices=TYPE_OF_CAMPAIGN)
    converted = models.IntegerField(default=0)
    # actions = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_random_id()
        super(Campaign, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lead(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONVERTED', 'Converted'),
        ('REJECTED', 'Rejected'),
    )

    id = models.CharField(max_length=4, primary_key=True,
                          unique=True, editable=False)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='campaign_lead', to_field='id')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')
    actions = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_random_id()
        super(Lead, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
