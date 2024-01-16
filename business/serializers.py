from rest_framework import serializers
from .models import Business, Campaign, Lead, Result


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
                  'phone_number', 'created', 'status')


class CampaginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id', 'title', 'leads',
                  'type_of', 'created', 'converted')


class GoogleSheetURLSerializer(serializers.Serializer):
    sheet_url = serializers.URLField()


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
