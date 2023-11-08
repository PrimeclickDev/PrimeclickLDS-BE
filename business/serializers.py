from rest_framework import serializers
from .models import Business, Campaign, Lead


class CampaignUploadSerializer(serializers.Serializer):
    campaign = serializers.FileField()


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'full_name', 'email', 'phone_number')


# class CampaginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Campaign
#         fields = ('id', 'title', 'leads', 'type_of_campaign', 'converted')

#     def create(self, validated_data):
