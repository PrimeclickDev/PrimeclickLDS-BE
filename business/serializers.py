from rest_framework import serializers

from accounts.utils import send_invite_lint_email
from .models import Business, CallReport, Campaign, FormDesign, Lead, ViewTimeHistory


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


class CollectEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    campaign_id = serializers.CharField(required=True)

    def create(self, validated_data):
        campaign_id = validated_data['campaign_id']
        email = validated_data['email']
        campaign = Campaign.objects.get(id=campaign_id)
        view_link_time = ViewTimeHistory.objects.create(
            campaign=campaign,
            email=email,
            # link=f"http://primeclick-autoleads.vercel.app/dashboard/{campaign_id}/{email}"
            link=f"https://primeclick-autoleads.vercel.app/leads/{campaign_id}"
        )
        link = view_link_time.link
        send_invite_lint_email(email, link)
        return view_link_time
