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
from infobip_utils.create_call import call
from infobip_utils.delete_call import call_delete
from infobip_utils.launch_call import launch
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import FormDesign, Lead, Campaign, Business, CallReport
from django.db import transaction
# from launch_call import arrange_nums, launch
import time
import io
import csv
from django.http import HttpResponse, JsonResponse
from .serializers import (CallAudioLinksSerializer, CampaignUploadSerializer, ContactOptionSerializer, FormDesignSerializer,
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
                    # Process phone numbers
                    phone_number = row[column]

                    # Check if phone_number is not None
                    if phone_number is not None:
                        # Convert to string and remove spaces
                        phone_number_str = str(phone_number).replace(" ", "")
                        pattern = re.compile(r'^(\d{1})?(\d{10})$')

                        # Check if the phone number matches the pattern
                        match = pattern.match(phone_number_str)
                        if match:
                    # If the phone number starts with '0', strip it and prepend '+234'
                            if match.group(1) == '0':
                                processed_phone_number = '+234' + match.group(2)
                            else:
                                # If it doesn't start with '0', directly prepend '+234'
                                processed_phone_number = '+234' + phone_number_str
                        else:
                    # If it doesn't match the pattern, handle the error or log it
                            print(f"Invalid phone number format: {phone_number_str}")
                    else:
                        # Handle the case when phone_number is None
                        processed_phone_number = None

                    lead_data['phone_number'] = processed_phone_number
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
        audio2 = user_data.get('audio_link_2')
        audio3 = user_data.get('audio_link_3')
        # scenario_id = call(audio1, audio2,  audio3)

        campaign = self.get_object()  # Retrieve the Campaign object
        serializer.save(
            # call_scenario_id=scenario_id,
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
        # Retrieve the Campaign object based on the provided campaign_id
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"message": "Campaign not found"}, status=404)

        # Extract numbers from the Leads associated with the Campaign
        leads_phone_numbers = Lead.objects.filter(
            campaign=campaign).values_list('phone_number', flat=True)
        nums = [number for number in leads_phone_numbers]
        print(nums)

        # scenario_id = campaign.call_scenario_id

        # Now you have the nums list and scenario_id, and you can use them in your further logic
        # For example, you can call the `launch` function passing the nums list and scenario_id
        try:
            make_voice_call(nums)
            # call_delete(scenario_id)
            return Response({"message": "Call launched and scenario deleted successfully"})
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

        lead = serializer.validated_data
        phone_number = lead['phone_number']

        # Process the phone number before saving to the database
        if phone_number is not None:
            # Convert to string and remove spaces
            phone_number_str = str(phone_number).replace(" ", "")
            pattern = re.compile(r'^(\d{1})?(\d{10})$')

            # Check if the phone number matches the pattern
            match = pattern.match(phone_number_str)
            if match:
        # If the phone number starts with '0', strip it and prepend '+234'
                if match.group(1) == '0':
                    processed_phone_number = '+234' + match.group(2)
                else:
                    # If it doesn't start with '0', directly prepend '+234'
                    processed_phone_number = '+234' + phone_number_str
            else:
        # If it doesn't match the pattern, handle the error or log it
                print(f"Invalid phone number format: {phone_number_str}")
        else:
            # Handle the case when phone_number is None
            processed_phone_number = None

        if processed_phone_number:
            lead['phone_number'] = processed_phone_number

            num = [processed_phone_number]
        else:
            num = []

        lead_instance = serializer.save(campaign=campaign)

        campaign.leads += 1
        campaign.save()
        # scenario_id = campaign.call_scenario_id

        try:
            make_voice_call(campaign_id, num)
            return Response({"message": "Call launched and scenario deleted successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

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

        # Get the leads for the specified campaign
        leads = Lead.objects.filter(campaign__id=campaign_id)

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
                'leads': leads_data,
            }
            print(response_data)

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Handle the case where there are no leads
            return Response({'status': 'success', 'message': 'No leads found'}, status=status.HTTP_200_OK)


class LeadDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # Use the serializer for individual lead details
    serializer_class = LeadListSerializer
    queryset = Lead.objects.all()  # Queryset for all leads
    lookup_field = 'id'
    lookup_url_kwarg = 'lead_id'

    # def get_object(self):
    #     # Get the lead_id from the URL
    #     lead_id = self.kwargs.get('lead_id')

    #     # Get the lead based on lead_id
    #     lead = get_object_or_404(self.get_queryset(), id=lead_id)

    #     return lead


class CampaignListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CampaginSerializer

    def get_queryset(self):
        # Get the campaign_id from the URL
        business_id = self.kwargs.get('business_id')
        # business = get_object_or_404(Business, id=business_id)
        campaigns = Campaign.objects.filter(business__id=business_id)
        # print(campaigns)

        return campaigns


class CallReportAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            data = request.data.get('results', [])[0]
            to_number = data.get('to')
            scenario_id = data.get('voiceCall', {}).get(
                'ivr', {}).get('scenarioId')
            print(data)

            campaign = Campaign.objects.get(call_scenario_id=scenario_id)
            lead = campaign.campaign_lead.filter(
                phone_number=to_number).first()
            call_report, created = CallReport.objects.get_or_create(
                lead=lead, campaign=campaign, report=data)

            if created:
                # If a new instance was created, update the lead status
                lead.status = "Contacted"
                if call_report.report.get('voiceCall', {}).get('dtmfCodes'):
                    call_report_status = call_report.report.get('voiceCall', {}).get('dtmfCodes').split(',')[
                        0]
                    if call_report_status == '1':
                        lead.contacted_status = "Converted"
                    elif call_report_status == '2':
                        lead.contacted_status = "Rejected"
                    else:
                        lead.contacted_status = "Rejected"
            else:
                # If an existing instance was retrieved, no need to update the lead status
                pass

            lead.save()
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FormDesignCreateAPIView(generics.CreateAPIView):
    serializer_class = FormDesignSerializer

    def perform_create(self, serializer):
        # Get the campaign_id from URL
        campaign_id = self.kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)

        # Check if a record already exists for this campaign
        existing_record = FormDesign.objects.filter(campaign=campaign).first()
        if existing_record:
            # If a record exists, inform the user
            raise serializers.ValidationError(
                "A form design already exists for this campaign.")
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
        print(destination_number)
        dest_number_campaign = Campaign.objects.filter(campaign_lead__phone_number=destination_number).first()
        print("PRINT CAMPAIGN HERE!")
        print(dest_number_campaign)
        if dest_number_campaign:
            audio_link_1 = dest_number_campaign.audio_link_1
            print(audio_link_1)
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
            dest_number_campaign = Campaign.objects.filter(campaign_lead__phone_number=destination_number).first()
            print("PRINT CAMPAIGN HERE!")
            print(dest_number_campaign)
            if dest_number_campaign:
                audio_link_2 = dest_number_campaign.audio_link_1
                audio_link_3 = dest_number_campaign.audio_link_3
            else:
                return Response({"error": "Requested campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if data  == "1" or data == 1:
                res = positive_flow(audio_link_2)
                return HttpResponse(res, content_type='text/xml')
            elif data == "2" or data == 2:
                res = negative_flow(audio_link_3)
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