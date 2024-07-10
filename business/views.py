import re
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
import pandas as pd
from AIT.xlm_res import intro_response, positive_flow, negative_flow, record_call
from AIT.ait import make_voice_call
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import logging
from backend import settings
from backend.utils import format_number_before_save
from infobip_utils.create_call import call
from infobip_utils.delete_call import call_delete
from infobip_utils.launch_call import launch
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import FormDesign, Lead, Campaign, Business
from django.db import transaction
# from launch_call import arrange_nums, launch
import time
import io
import csv
from django.http import HttpResponse, JsonResponse

from .permissions import IsLinkValid
from .serializers import (CallAudioLinksSerializer, CampaignUploadSerializer, ContactOptionSerializer,
                          FormDesignSerializer,
                          LeadFormSerializer,
                          LeadListSerializer,
                          LeadUploadSerializer,
                          CampaignNameSerializer,
                          CampaginSerializer,
                          GoogleSheetURLSerializer, CollectEmailSerializer)
logger = logging.getLogger(__name__)

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

        # Iterate over each row in the CSV file
        for _, row in reader.iterrows():
            lead_data = {}
            for column in reader.columns:
                # Check if the column contains the keyword 'name' or 'phone' (case-insensitive)
                if 'name' in column.lower():
                    lead_data['full_name'] = row[column]
                elif 'phone' in column.lower():
                    # Process phone numbers
                    phone_number = row[column]

                    processed_number = format_number_before_save(phone_number)
                    if processed_number:
                        lead_data['phone_number'] = processed_number

                elif 'email' in column.lower():
                    lead_data['email'] = row[column]
                # Add more conditions for other keywords or fields as needed

            # Associate each lead with the newly created campaign
            lead_data['campaign'] = new_campaign
            lead = Lead(**lead_data)
            lead.save()
            # total_lead_count += 1

        # Update the total_leads field in the campaign
        new_campaign.leads = Lead.objects.filter(campaign=new_campaign).count()
        new_campaign.save()

        response_data = {"status": "success", "campaign_id": new_campaign.id}

        return Response(response_data, status=status.HTTP_201_CREATED)


class ContactOptionAPIView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ContactOptionSerializer

    def get_object(self):
        campaign_id = self.kwargs.get("campaign_id")
        return Campaign.objects.get(id=campaign_id)


class CallCreateAPIView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CallAudioLinksSerializer

    def get_object(self):
        campaign_id = self.kwargs.get("campaign_id")
        return Campaign.objects.get(id=campaign_id)

    def perform_update(self, serializer):
        user_data = self.request.data
        audio1 = user_data.get('audio_link_1')
        print("CHECKING---------", audio1)
        audio2 = user_data.get('audio_link_2')
        audio3 = user_data.get('audio_link_3')

        campaign = self.get_object()
        serializer.save(
            audio_link_1=audio1,
            audio_link_2=audio2,
            audio_link_3=audio3
        )

        return Response(
            {"message": "Update successful", "campaign_id": campaign.id},  # Use campaign.id
            status=status.HTTP_200_OK
        )


class LaunchCallAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id, *args, **kwargs):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"message": "Campaign not found"}, status=404)

        # Extract numbers from the Leads associated with the Campaign
        leads_phone_numbers = Lead.objects.filter(
            campaign=campaign).values_list('phone_number', flat=True)
        nums = [number for number in leads_phone_numbers]
        print(nums)

        try:
            make_voice_call(nums, campaign_id)
            return Response({"message": "Call launched successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


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

        lead_data = serializer.validated_data
        phone_number = lead_data.get('phone_number')

        processed_number = format_number_before_save(phone_number)

        if processed_number:
            lead_data['phone_number'] = processed_number
        else:
            pass

        lead_instance = Lead.objects.create(campaign=campaign, **lead_data)

        campaign.leads = Lead.objects.filter(campaign=campaign).count()
        campaign.save()

        # Call the function
        num = [processed_number] if processed_number else []
        try:
            make_voice_call(num, campaign_id)
            return Response({"message": "Call launched and scenario deleted successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class LeadListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LeadListSerializer

    def get_queryset(self):
        # Get the campaign_id from the URL
        campaign_id = self.kwargs.get('campaign_id')

        # Get the leads for the specified campaign
        leads = Lead.objects.filter(campaign__id=campaign_id).select_related("campaign")

        return leads

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Check if there are leads in the queryset
        if queryset.exists():
            leads_data = []

            for lead in queryset:
                lead_data = LeadListSerializer(lead).data
                leads_data.append(lead_data)

            response_data = {
                'campaign_name': queryset[0].campaign.title,
                'campaign_id': queryset[0].campaign.id,
                'leads': leads_data
            }
            print(response_data)

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Handle the case where there are no leads
            return Response({'status': 'success', 'message': 'No leads found'}, status=status.HTTP_200_OK)


class LeadDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    # Use the serializer for individual lead details
    serializer_class = LeadListSerializer
    queryset = Lead.objects.all()  # Queryset for all leads
    lookup_field = 'id'
    lookup_url_kwarg = 'lead_id'


class CampaignListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CampaginSerializer

    def get_queryset(self):
        # Get the campaign_id from the URL
        business_id = self.kwargs.get('business_id')
        # business = get_object_or_404(Business, id=business_id)
        campaigns = Campaign.objects.filter(business__id=business_id)
        # print(campaigns)

        return campaigns


class FormDesignCreateAPIView(generics.CreateAPIView):
    serializer_class = FormDesignSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        # Get the campaign_id from URL
        campaign_id = self.kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)

        # Check if a record already exists for this campaign
        existing_record = FormDesign.objects.filter(campaign=campaign).first()
        if existing_record:
            # If a record exists, inform the user
            raise serializers.ValidationError(
                "A form design already exists for this campaign.", code=status.HTTP_409_CONFLICT)
        else:
            # If no record exists, create a new one
            serializer.save(campaign=campaign)

    def post(self, request, *args, **kwargs):
        # Call the parent class post method to perform creation
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data['message'] = "Form design saved successfully"
        return response


class FormDesignRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    # Use the serializer for individual lead details
    serializer_class = FormDesignSerializer
    queryset = FormDesign.objects.all()  # Queryset for all leads

    def get_object(self):
        # Get the lead_id from the URL
        campaign_id = self.kwargs.get('campaign_id')

        # Get the lead based on lead_id
        design = get_object_or_404(
            self.get_queryset(), campaign_id=campaign_id)

        return design


class FormDesignUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = FormDesign.objects.all()
    serializer_class = FormDesignSerializer

    # lookup_field = 'campaign_id'

    def get_object(self):
        campaign_id = self.kwargs.get("campaign_id")
        design = get_object_or_404(Campaign, id=campaign_id)
        return design

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form design updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})


class AITAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        destination_number = request.data.get("callerNumber")
        session_id = request.data.get("sessionId")
        print("SESSION ID HERE-------", session_id)

        # if session_id:
        #     session_id = str(session_id).strip()

        # Fetch the lead with the related campaign in a single query
        lead = Lead.objects.select_related('campaign').filter(session_id=session_id,
                                                              phone_number=destination_number).first()
        print("LEAD HERE-------", lead)

        if lead:
            # Access the related campaign from the lead object
            dest_number_campaign = lead.campaign
            lead.status = "Contacted"
            lead.save()
        else:
            dest_number_campaign = None

        if dest_number_campaign:
            audio_link_1 = dest_number_campaign.audio_link_1
            xml_data = intro_response(audio_link_1)
            return HttpResponse(xml_data, content_type='text/xml')
        else:
            return Response({"error": "Requested campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)


class AITFlowAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.get("dtmfDigits")
            destination_number = request.data.get("callerNumber")
            # record_url = request.data.get("recordingUrl")
            session_id = request.data.get("sessionId")
            lead = Lead.objects.select_related('campaign').filter(session_id=session_id,
                                                                  phone_number=destination_number).first()
            # print("RECORDING ---------- ", record_url)
            dest_number_campaign = lead.campaign
            if dest_number_campaign:
                audio_link_2 = dest_number_campaign.audio_link_2
                audio_link_3 = dest_number_campaign.audio_link_3
            else:
                return Response({"error": "Requested campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if data == "1" or data == 1:
                res = positive_flow(audio_link_2)
                lead.contacted_status = "Converted"
                lead.campaign.converted += 1
                lead.save()
                return HttpResponse(res, content_type='text/xml')
            elif data == "2" or data == 2:
                res = negative_flow(audio_link_3)
                lead.contacted_status = "Rejected"
                lead.save()
                return HttpResponse(res, content_type='text/xml')
            else:
                # Provide a default response if the condition isn't met
                return Response({"message": "Invalid or missing dtmfDigits value"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handling other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AITRecordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        xml_data = request.data
        print(xml_data)
        return Response({"message": "File data gotten!"})


class GoogleSheetWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        api_key = request.headers.get('Api-Key')
        if api_key != settings.SECRET_KEY:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        print("THIS IS THE RAW DATA", data)

        # Ensure data is structured correctly
        if 'data' not in data or not isinstance(data['data'], dict):
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

        for campaign_id, rows in data['data'].items():
            print("Campaign ID:", campaign_id)

            # Find or create the campaign based on campaign_id
            campaign = Campaign.objects.filter(id=campaign_id).first()
            if not campaign:
                return Response({"error": f"Campaign '{campaign_id}' not found"}, status=status.HTTP_404_NOT_FOUND)

            for row in rows:
                full_name = row.get('FULL NAME', '').strip()
                email = row.get('EMAIL', '').strip()
                phone_number = row.get('PHONE NUMBER', '').strip()

                # Validate and process each field as needed
                processed_number = format_number_before_save(phone_number)

                # Create lead record
                lead_data = {
                    'campaign': campaign,
                    'full_name': full_name,
                    'email': email,
                    'phone_number': processed_number if processed_number else None
                }
                Lead.objects.create(**lead_data)

                # Perform additional actions (e.g., making a voice call)
                try:
                    if processed_number:
                        make_voice_call([processed_number], campaign.id)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Update campaign stats
                campaign.leads = Lead.objects.filter(campaign=campaign).count()
                campaign.save()

        return Response({"message": "Data processed successfully"})



class CollectEmailView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        serializer = CollectEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Link sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadsViewOnlyView(generics.ListAPIView):
    serializer_class = LeadListSerializer
    permission_classes = [IsLinkValid]

    def get_queryset(self):
        campaign_id = self.kwargs.get('campaign_id')
        return Lead.objects.filter(campaign__id=campaign_id).select_related('campaign')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset.exists():
            leads_data = [LeadListSerializer(lead).data for lead in queryset]
            response_data = {
                'campaign_name': queryset[0].campaign.title,
                'leads': leads_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'success', 'message': 'No leads found'}, status=status.HTTP_200_OK)
