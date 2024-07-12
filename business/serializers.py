import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from urllib.parse import urlencode
from accounts.utils import send_invite_lint_email
from .models import Business, CallReport, Campaign, FormDesign, Lead, ViewTimeHistory
from django.contrib.sites.shortcuts import get_current_site


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('id', 'name', 'email', 'avatar', 'description')


class CampaignUploadSerializer(serializers.Serializer):
    campaign = serializers.FileField()


class CampaignNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class LeadUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'full_name', 'email', 'phone_number')


class LeadFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('full_name', 'email', 'phone_number')


class LeadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'full_name', 'email',
                  'phone_number', 'created', 'status', 'contacted_status')


class CampaginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id', 'title', 'leads',
                  'type_of', 'created', 'converted')


class GoogleSheetURLSerializer(serializers.Serializer):
    sheet_url = serializers.URLField()


class CallReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallReport
        fields = '__all__'


class ContactOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("contact_option",)


class CallAudioLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("audio_link_1",
                  "audio_link_2", "audio_link_3", "audio_link_4")


class FormDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDesign
        fields = ("design",)



def generate_random_token(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class InviteEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    campaign_id = serializers.CharField(required=True)

    def create(self, validated_data):
        campaign_id = validated_data['campaign_id']
        email = validated_data['email']
        request = self.context.get('request')

        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except ObjectDoesNotExist:
            raise ValueError("Campaign does not exist.")

        with transaction.atomic():
            old_link = ViewTimeHistory.objects.filter(campaign=campaign, email=email)
            if old_link:
                old_link.delete()

            # Generate tokens
            path_token = generate_random_token(32)
            access_code = generate_random_token(6)

            # Create link with path token
            link = f"http://primeclick-autoleads.vercel.app/guest/dashboard/{campaign_id}"

            view_link_time = ViewTimeHistory.objects.create(
                campaign=campaign,
                email=email,
                link=link,
                access_code=access_code
            )
        current_site = get_current_site(request)
        domain = current_site.domain
        site_url = f"https://{domain}"
        # Send email with link and access code
        try:
            send_invite_lint_email(email, link, access_code, site_url, campaign_name=campaign.title)
        except Exception as e:
            # Handle the exception (e.g., log it, retry sending the email, etc.)
            raise RuntimeError("Failed to send email.") from e

        return view_link_time

