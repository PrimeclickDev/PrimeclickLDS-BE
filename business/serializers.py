import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from urllib.parse import urlencode
from accounts.utils import send_invite_lint_email
from .models import Business, CallReport, Campaign, FormDesign, Lead, ViewTimeHistory, ActivityLog, Support
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
                  'phone_number', 'created', 'status', 'contacted_status', 'recording_url', 'call_time', 'call_duration')


class CampaginSerializer(serializers.ModelSerializer):
    contacted_leads = serializers.IntegerField(read_only=True)
    converted_leads = serializers.IntegerField(read_only=True)
    class Meta:
        model = Campaign
        fields = ('id', 'title', 'leads',
                  'type_of', 'created', 'converted', 'contacted_leads', 'converted_leads')


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

class ContentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("content_option",)


class CallAudioLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("audio_link_1",
                  "audio_link_2", "audio_link_3", "audio_link_4")


class CallTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("text_1",
                  "text_2", "text_3", "text_4")


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
            link = f"https://autoleads.primeclickmedia.com/guest/campaigns/{campaign_id}"

            view_link_time = ViewTimeHistory.objects.create(
                campaign=campaign,
                email=email,
                link=link,
                access_code=access_code,
                has_access=True
            )
        try:
            send_invite_lint_email(email, link, access_code, campaign_name=campaign.title)
        except Exception as e:
            # Handle the exception (e.g., log it, retry sending the email, etc.)
            raise RuntimeError("Failed to send email.") from e

        return view_link_time


class ViewAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewTimeHistory
        fields = "__all__"


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = "__all__"


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['id', 'user', 'email', 'subject', 'description', 'resolved']
        read_only_fields = ['resolved']  # Users can't change the resolved status


class AdminSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['id', 'user', 'email', 'issue', 'resolved']
        read_only_fields = ['user', 'email', 'subject', 'description']  # Admin cannot change issue details

