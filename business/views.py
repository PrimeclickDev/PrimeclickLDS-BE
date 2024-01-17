from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
import pandas as pd
from backend.settings import GOOGLE_SHEET_API_CREDS
from rest_framework.response import Response
from rest_framework import status
from .googlesheets import get_google_sheets_data
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Lead, Campaign, Business, CallReport
import io
import csv
from django.http import JsonResponse
from .serializers import (CampaignUploadSerializer,
                          LeadFormSerializer,
                          LeadListSerializer,
                          LeadUploadSerializer,
                          CampaignNameSerializer,
                          CampaginSerializer,
                          GoogleSheetURLSerializer, CallReportSerializer)


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

            # Associate each lead with the newly created campaign
            lead_data['campaign'] = new_campaign
            lead = Lead(**lead_data)
            lead.save()
            total_lead_count += 1

        # Update the total_leads field in the campaign
        new_campaign.leads = total_lead_count
        new_campaign.save()

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)


class GoogleSheetUploadView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = GoogleSheetURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sheet_url = serializer.validated_data['sheet_url']
        credentials_path = GOOGLE_SHEET_API_CREDS

        # Get data from Google Sheets
        data = get_google_sheets_data(sheet_url, credentials_path)

        # Extract sheet name (assuming it's the first sheet in the workbook)
        sheet_name = data.title

        # Extract business_id from URL (you need to implement this logic based on your URL structure)
        business_id = kwargs.get('business_id')

        # Create or get Business instance
        business, created = Business.objects.get_or_create(id=business_id)

        # Create a new Campaign
        new_campaign = Campaign.objects.create(
            title=sheet_name,
            business=business,
            type_of='UPLOAD'
        )

        # Process and save data to the Lead model
        # Assuming the first row contains headers (field names)
        # Convert to lowercase for case-insensitive matching
        headers = [header.lower() for header in data[0]]
        leads_data = data[1:]

        # Mapping dictionary for header names to model field names
        header_mapping = {
            'name': 'full_name',
            'email': 'email',
            'phone': 'phone_number',
            # Add more mappings as needed
        }

        for lead_data in leads_data:
            lead_dict = {header_mapping.get(
                header.lower(), header): value for header, value in zip(headers, lead_data)}

            Lead.objects.create(
                campaign=new_campaign,
                full_name=lead_dict.get('full_name', ''),
                email=lead_dict.get('email', ''),
                phone_number=lead_dict.get('phone_number', ''),
            )

        # Update the total_leads field in the campaign
        new_campaign.leads = len(leads_data)
        new_campaign.save()

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)


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
    permission_classes = [AllowAny]
    serializer_class = LeadFormSerializer

    def perform_create(self, serializer):
        campaign_id = self.kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Check if there are leads in the queryset
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)

            # Modify this response_data based on your requirements
            response_data = {
                'campaign_name': queryset.first().campaign.title,
                'leads': serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Handle the case where there are no leads
            return Response({'status': 'success', 'message': 'No leads found'}, status=status.HTTP_200_OK)


class LeadDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # Use the serializer for individual lead details
    serializer_class = LeadListSerializer
    queryset = Lead.objects.all()  # Queryset for all leads

    def get_object(self):
        # Get the lead_id from the URL
        lead_id = self.kwargs.get('lead_id')

        # Get the lead based on lead_id
        lead = get_object_or_404(self.get_queryset(), id=lead_id)

        return lead


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


class CallReportAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data['results'][0]
            voice_call_data = data.get('voiceCall', {})
            ivr_data = voice_call_data.get('ivr', {})
            status_data = data.get('status', {})
            error_data = data.get('error', {})

            extracted_data = {
                'bulk_id': data.get('bulkId'),
                'message_id': data.get('messageId'),
                'from_number': data.get('from'),
                'to_number': data.get('to'),
                'sent_at': data.get('sentAt'),
                'mcc_mnc': data.get('mccMnc'),
                'call_back_data': data.get('callbackData'),
                'feature': voice_call_data.get('feature'),
                'start_time': voice_call_data.get('startTime'),
                'answer_time': voice_call_data.get('answerTime'),
                'end_time': voice_call_data.get('endTime'),
                'duration': voice_call_data.get('duration'),
                'charged_duration': voice_call_data.get('chargedDuration'),
                'file_duration': voice_call_data.get('fileDuration'),
                'dtmf_codes': voice_call_data.get('dtmfCodes'),
                'scenario_id': ivr_data.get('scenarioId'),
                'scenario_name': ivr_data.get('scenarioName'),
                'group_id': status_data.get('groupId'),
                'group_name': status_data.get('groupName'),
                'status_id': status_data.get('id'),
                'status_name': status_data.get('name'),
                'status_description': status_data.get('description'),
                'error_group_id': error_data.get('groupId'),
                'error_group_name': error_data.get('groupName'),
                'error_id': error_data.get('id'),
                'error_name': error_data.get('name'),
                'error_description': error_data.get('description'),
                'error_permanent': error_data.get('permanent'),
            }

            for key, value in extracted_data.items():
                if value is None:
                    extracted_data[key] = None

            print(extracted_data)
            # Saving the extracted data directly into the database
            CallReport.objects.create(**extracted_data)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
