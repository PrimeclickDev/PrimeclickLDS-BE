from django.shortcuts import get_object_or_404, render
from rest_framework import generics
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Lead, Campaign, Business
from .serializers import CampaignUploadSerializer, LeadSerializer
import io
import csv


class CampaignUploadView(generics.CreateAPIView):
    permission_classes = [AllowAny]
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
            type_of_campaign='UPLOAD'
        )

        total_lead_count = 0

        for _, row in reader.iterrows():
            # Associate each lead with the newly created campaign
            lead = Lead(
                full_name=row["full_name"],
                email=row['email'],
                phone_number=row["phone_number"],
                campaign=new_campaign,
            )
            lead.save()
            total_lead_count += 1

        # Update the total_leads field in the campaign
        new_campaign.leads = total_lead_count
        new_campaign.save()

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
