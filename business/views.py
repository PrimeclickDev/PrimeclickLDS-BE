from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Lead, Campaign, Business
from .serializers import CampaignUploadSerializer, LeadFormSerializer, LeadListSerializer, LeadUploadSerializer, CampaignNameSerializer, CampaginSerializer
import io
import csv


class CampaignUploadView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignUploadSerializer

    def post(self, request, *args, **kwargs):
        business_id = self.kwargs.get('business_id')
        business = get_object_or_404(Business, id=business_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign = serializer.validated_data['campaign']

        if campaign.name.endswith('.csv'):
            # Read CSV file
            reader = pd.read_csv(campaign)
        elif campaign.name.endswith('.xlsx'):
            # Read Excel file
            reader = pd.read_excel(campaign, engine='openpyxl')
        else:
            return Response({"error": "Unsupported file format"}, status=status.HTTP_UNSUPPORTED_MEDIA_TYPE)

        # Create a new Campaign
        new_campaign = Campaign.objects.create(
            title=campaign.name,
            business=business,
            type_of='UPLOAD'
        )

        total_lead_count = 0

        for _, row in reader.iterrows():
            lead_data = {}
            for column in reader.columns:
                # Check if the column contains the keyword 'name' or 'phone' (case-insensitive)
                if 'name' in column.lower():
                    lead_data['full_name'] = row[column]
                elif 'phone' in column.lower():
                    lead_data['phone_number'] = row[column]
                elif 'email' in column.lower():
                    lead_data['email'] = row[column]
                # Add more conditions for other keywords or fields as needed

            # Create a new Campaign
            # new_campaign = Campaign.objects.create(
            #     title=campaign.name,
            #     business=business,
            #     type_of='UPLOAD'
            # )

            # Associate each lead with the newly created campaign
            lead_data['campaign'] = new_campaign
            lead = Lead(**lead_data)
            lead.save()
            total_lead_count += 1

        # Update the total_leads field in the campaign
        new_campaign.leads = total_lead_count
        new_campaign.save()

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)


class CampaignNameAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CampaignNameSerializer

    def post(self, request, *args, **kwargs):
        business_id = self.kwargs.get('business_id')
        business = get_object_or_404(Business, id=business_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']

        campaign = Campaign.objects.create(
            title=name,
            business=business,
            type_of='DIRECT'
        )

        response_data = {
            "campaign_id": campaign.id,
            "message": "Campaign created successfully"
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class LeadFormAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeadFormSerializer

    def perform_create(self, serializer):
        campaign_id = self.kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)

        # Create the Lead instance and associate it with the campaign
        lead = serializer.save(campaign=campaign)

        # Update the number of leads in the campaign
        campaign.leads += 1
        campaign.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {"message": "Lead added successfully"}
        return Response(response_data, status=status.HTTP_200_OK)


class LeadListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LeadListSerializer

    def get_queryset(self):
        # Get the campaign_id from the URL
        campaign_id = self.kwargs.get('campaign_id')

        # Get the campaign and its related leads
        campaign = get_object_or_404(Campaign, id=campaign_id)
        leads = Lead.objects.filter(campaign=campaign)

        return leads


class CampaignListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CampaginSerializer

    def get_queryset(self):
        # Get the campaign_id from the URL
        business_id = self.kwargs.get('business_id')
        business = get_object_or_404(Business, id=business_id)
        campaigns = Campaign.objects.filter(business=business)
        # print(campaigns)

        return campaigns
