import re
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
import requests
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, filters
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
import pandas as pd
from AIT.xlm_res import intro_response, positive_record, thank_you, handle_inbound
from AIT.ait import make_voice_call
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import logging
from backend import settings
from backend.utils import format_number_before_save
# from infobip_utils.create_call import call
# from infobip_utils.delete_call import call_delete
# from infobip_utils.launch_call import launch
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import FormDesign, Lead, Campaign, Business, ViewTimeHistory, random_id
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
                          GoogleSheetURLSerializer, InviteEmailSerializer, ContentOptionSerializer, CallTextSerializer)

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
            campaign_title = campaign.name[:-4]
            # Read CSV file
            reader = pd.read_csv(campaign)
        elif campaign.name.endswith('.xlsx'):
            campaign_title = campaign.name[:-5]
            # Read Excel file
            reader = pd.read_excel(campaign, engine='openpyxl')
        else:
            return Response({"error": "Unsupported file format"}, status=status.HTTP_UNSUPPORTED_MEDIA_TYPE)

        # Create a new Campaign
        try:
            with transaction.atomic():
                new_campaign = Campaign.objects.create(
                    title=campaign_title,
                    business=business,
                    type_of='UPLOAD'
                )

                total_lead_count = 0
                batch_size = 100  # Define your batch size here
                leads_batch = []

                # Iterate over each row in the file
                for _, row in reader.iterrows():
                    lead_data = {}
                    for column in reader.columns:
                        if 'name' in column.lower():
                            lead_data['full_name'] = row[column]
                        elif 'phone' in column.lower():
                            phone_number = row[column]
                            processed_number = format_number_before_save(phone_number)
                            if processed_number:
                                lead_data['phone_number'] = processed_number
                        elif 'email' in column.lower():
                            lead_data['email'] = row[column]

                    lead_data['campaign'] = new_campaign
                    lead_data['id'] = random_id()
                    lead = Lead(**lead_data)
                    leads_batch.append(lead)
                    total_lead_count += 1

                    # Once the batch size is reached, bulk create leads
                    if len(leads_batch) >= batch_size:
                        Lead.objects.bulk_create(leads_batch)
                        leads_batch = []  #

                # Create remaining leads if any
                if leads_batch:
                    Lead.objects.bulk_create(leads_batch)

                # Update the total_leads field in the campaign
                new_campaign.leads = total_lead_count
                new_campaign.save()

            response_data = {"status": "success", "campaign_id": new_campaign.id}
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Handle the exception
            print(f"An error occurred: {e}")
            return Response({"error": "An error occurred while processing the campaign"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactOptionAPIView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ContactOptionSerializer

    def get_object(self):
        campaign_id = self.kwargs.get("campaign_id")
        return Campaign.objects.get(id=campaign_id)


class ContentOptionAPIView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ContentOptionSerializer

    def get_object(self):
        campaign_id = self.kwargs.get("campaign_id")
        return Campaign.objects.get(id=campaign_id)


class CallCreateAPIView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Get the campaign to check its content type
        campaign = self.get_object()

        # Assuming content_type is a field that determines if it's 'audio' or 'text'
        if campaign.content_option == "Audio":
            return CallAudioLinksSerializer
        elif campaign.content_option == "Text":
            return CallTextSerializer
        else:
            return Response(
                {"error": "Invalid content option"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self):
        campaign_id = self.kwargs.get("campaign_id")
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            return campaign
        except Campaign.DoesNotExist:
            return Response(
                {"error": "Campaign doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def perform_update(self, serializer):
        campaign = self.get_object()
        # The serializer already knows which fields to handle based on the content type
        serializer.save()

        return Response(
            {"message": "Update successful", "campaign_id": campaign.id},
            status=status.HTTP_200_OK
        )


class LaunchCallAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id, *args, **kwargs):
        start_time = time.time()

        # Try to get the campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"message": "Campaign not found"}, status=404)

        # Define the cache key based on the campaign_id
        cache_key = f'leads_phone_numbers_{campaign_id}'

        # Try to get phone numbers from the cache
        nums = cache.get(cache_key)

        # If not cached, query the database and cache the results
        if nums is None:
            leads_phone_numbers = Lead.objects.filter(
                campaign=campaign
            ).exclude(Q(contacted_status="Converted") | Q(contacted_status="Rejected")).values_list(
                'phone_number', flat=True
            )
            nums = [number for number in leads_phone_numbers if number is not None]
            cache.set(cache_key, nums, timeout=60 * 10080)  # Cache for 10 minutes (adjust as needed)

        print(f"Processing {len(nums)} numbers")
        batch_size = 20

        def process_batch(batch_nums):
            try:
                make_voice_call(batch_nums, campaign_id)
            except Exception as e:
                print(f"Error processing batch: {e}")

        with ThreadPoolExecutor(max_workers=5) as executor:
            for i in range(0, len(nums), batch_size):
                batch_nums = nums[i:i + batch_size]
                executor.submit(process_batch, batch_nums)

        elapsed_time = time.time() - start_time
        print(f"Total time for processing: {elapsed_time} seconds")

        return Response({"message": "Calls launched successfully"}, status=200)


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
        with transaction.atomic():
            lead_instance = Lead.objects.create(campaign=campaign, **lead_data)

            # Safely update the lead count within the transaction
            campaign.leads_count = Lead.objects.filter(campaign=campaign).count()
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
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name"]

    def get_queryset(self):
        # Get the campaign_id from the URL
        campaign_id = self.kwargs.get('campaign_id')

        # Generate a cache key based on campaign_id
        cache_key = f"leads_{campaign_id}"

        # Try to get the cached queryset
        leads = cache.get(cache_key)

        if leads is None:
            # If the user is not staff, check if the campaign exists and the user is associated with the business
            if not self.request.user.is_staff:
                if not Campaign.objects.filter(id=campaign_id, business__users=self.request.user).exists():
                    raise NotFound(detail="Campaign not found or you do not have permission to access it.")

            # Filter leads by campaign_id
            leads = Lead.objects.filter(campaign__id=campaign_id).select_related("campaign")

            # Cache the queryset results for 15 minutes
            cache.set(cache_key, leads, timeout=60 * 10080)

        return leads

    def list(self, request, *args, **kwargs):
        # Check if there are leads in the queryset
        queryset = self.get_queryset()
        if queryset.exists():
            leads_data = [LeadListSerializer(lead).data for lead in queryset]

            response_data = {
                'campaign_name': queryset[0].campaign.title,
                'campaign_id': queryset[0].campaign.id,
                'leads': leads_data
            }

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
        # Get the business_id from the URL
        business_id = self.kwargs.get('business_id')
        # cache_key = f"leads_{campaign_id}"

        if self.request.user.is_staff:
            # If the user is staff, return campaigns for the specified business
            campaigns = Campaign.objects.filter(business__id=business_id)
        else:
            # If the user is not staff, return campaigns for the specified business only if the user is associated with the business
            campaigns = Campaign.objects.filter(business__id=business_id, business__users=self.request.user)

        return campaigns


class FormDesignCreateAPIView(generics.CreateAPIView):
    serializer_class = FormDesignSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        # Get the campaign_id from URL
        campaign_id = self.kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)

        # Check if a record already exists for this campaign
        if FormDesign.objects.filter(campaign=campaign).exists():
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
        print("DID IT GET HERE AT ALL????????")
        destination_number = request.data.get("callerNumber")
        session_id = request.data.get("sessionId")
        print("SESSION ID HERE-------", session_id)
        print("PHONE NUMBER HERE---------", destination_number)
        direction = request.data.get("direction")

        # if session_id:
        #     session_id = str(session_id).strip()

        # Fetch the lead with the related campaign in a single query
        lead = Lead.objects.select_related('campaign').filter(
            phone_number=destination_number).first()
        # print("CHECK IF SESSION ID:", session_id==lead.session_id)
        print("LEAD HERE-------", lead)

        if direction == "Inbound":
            inb_xml_data = handle_inbound()
            return HttpResponse(inb_xml_data, content_type='application/xml')

        if lead:
            # Access the related campaign from the lead object
            dest_number_campaign = lead.campaign
            lead.status = "Contacted"
            lead.save()
        else:
            dest_number_campaign = None

        if dest_number_campaign:
            audio_link_1 = dest_number_campaign.audio_link_1
            try:
                # xml_data = intro_response(audio_link_1)
                xml_data = intro_response() #test
                return HttpResponse(xml_data, content_type='application/xml')
            except Exception as e:
                print(e)
        else:
            return Response({"error": "Requested campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)


class AITFlowAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.get("dtmfDigits")
            destination_number = request.data.get("callerNumber")
            session_id = request.data.get("sessionId")
            direction = request.data.get("direction")
            lead = Lead.objects.select_related('campaign').filter(
                phone_number=destination_number).first()

            dest_number_campaign = lead.campaign
            if dest_number_campaign:
                audio_link_2 = dest_number_campaign.audio_link_2
                audio_link_3 = dest_number_campaign.audio_link_3

            if data == "1":
                # res = positive_record(audio_link_2)
                res = positive_record()
                lead.contacted_status = "Converted"
                lead.save()
                cache_key = f"leads_{lead.campaign.id}"
                cache.delete(cache_key)
                # thank_you(audio_link_3)
                return HttpResponse(res, content_type='application/xml')
            else:
                lead.contacted_status = "Rejected"
                # Provide a default response if the condition isn't met
                return Response({"message": "Call Rejected Without DTMF"}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handling other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AITRecordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        destination_number = request.data.get("callerNumber")
        session_id = request.data.get("sessionId")
        recording_url = request.data.get('recordingUrl', '')
        call_start_time = request.data.get('callStartTime')
        call_duration = request.data.get('durationInSeconds')

        # Log incoming data
        print(f"Received Data: session_id={session_id}, destination_number={destination_number}, "
              f"recording_url={recording_url}, call_start_time={call_start_time}, call_duration={call_duration}")

        try:
            lead = Lead.objects.select_related('campaign').filter(
                phone_number=destination_number).first()
            if lead is None:
                return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

            dest_number_campaign = lead.campaign
            audio3 = dest_number_campaign.audio_link_3

            if not lead.recording_url:
                lead.recording_url = recording_url

            if not lead.call_time:
                lead.call_time = call_start_time

            if not lead.call_duration:
                lead.call_duration = call_duration

            lead.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Use thank_you response and return it as XML
        xml_response = thank_you()
        print(f"XML Response: {xml_response}")  # Debugging output

        # Return the XML response using DRF's Response
        return HttpResponse(xml_response, content_type="application/xml")


class RecordingProxyAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, lead_id):
        # Fetch the Lead object
        lead = get_object_or_404(Lead, id=lead_id)

        # Get the raw HTTP URL from the Lead object
        recording_url = lead.recording_url
        if not recording_url:
            return Response({"error": "No recording URL found for this lead."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the content from the original URL
        external_response = requests.get(recording_url)

        if external_response.status_code == 200:
            # Set the correct content type for the audio file
            content_type = external_response.headers.get('Content-Type', 'audio/mpeg')

            # Set the response headers for the audio file
            response_headers = {
                'Content-Type': content_type,
                'Content-Disposition': 'inline',  # This tells the browser to display/play the content
            }

            # Return the response with binary content and headers
            return HttpResponse(external_response.content, headers=response_headers)
        else:
            return Response(
                {"error": f"Failed to fetch the content from {recording_url}"},
                status=external_response.status_code
            )

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

        try:
            with transaction.atomic():
                for campaign_id, rows in data['data'].items():
                    print("Campaign ID:", campaign_id)

                    # Find the campaign based on campaign_id
                    campaign = Campaign.objects.filter(id=campaign_id).first()
                    if not campaign:
                        return Response({"error": f"Campaign '{campaign_id}' not found"},
                                        status=status.HTTP_404_NOT_FOUND)

                    for row in rows:
                        full_name = row.get('FULL NAME', '').strip()
                        email = row.get('EMAIL', '').strip()
                        phone_number = row.get('PHONE NUMBER', '').strip()

                        # Validate and process each field as needed
                        processed_number = format_number_before_save(phone_number)
                        print(f"Processed Number: {processed_number}")

                        check_lead = Lead.objects.filter(
                            Q(campaign=campaign) & (Q(status="Pending") | Q(contacted_status="Pending"))
                        )
                        if check_lead.exists():
                            retry_nums = [lead.phone_number for lead in check_lead]

                            try:
                                make_voice_call(retry_nums, campaign.id)
                            except Exception as e:
                                print(f"Voice call error: {e}")

                        # Create lead record
                        if not Lead.objects.filter(
                                campaign=campaign,
                                full_name=full_name,
                                email=email,
                                phone_number=processed_number
                        ).exists():
                            # Create lead record if it doesn't exist
                            lead_data = {
                                'campaign': campaign,
                                'full_name': full_name,
                                'email': email,
                                'phone_number': processed_number if processed_number else None
                            }
                            Lead.objects.create(**lead_data)
                            print(f"Created Lead: {lead_data}")

                        # Perform additional actions (e.g., making a voice call)
                        try:
                            if processed_number:
                                make_voice_call([processed_number], campaign.id)
                        except Exception as e:
                            print(f"Additional voice call error: {e}")
                            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # Update campaign stats
                    campaign.leads = Lead.objects.filter(campaign=campaign).count()
                    campaign.save()
                    print(f"Updated Campaign Leads: {campaign.leads}")
        except Exception as e:
            print(f"Transaction error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Data processed successfully"})


class CollectEmailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = InviteEmailSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Link sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadsViewOnlyView(generics.ListAPIView):
    serializer_class = LeadListSerializer
    permission_classes = [AllowAny, IsLinkValid]
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name"]

    def get_queryset(self):
        campaign_id = self.kwargs.get('campaign_id')

        if campaign_id is None:
            raise ValueError("campaign_id is required")

        try:
            leads = Lead.objects.filter(campaign__id=campaign_id).select_related('campaign')
        except Lead.DoesNotExist:
            leads = Lead.objects.none()  # Return an empty queryset if no leads are found
        except Exception as e:
            # Log the exception, handle it appropriately or re-raise it
            print(f"An error occurred: {e}")
            leads = Lead.objects.none()  # Optionally return an empty queryset

        return leads

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset := self.get_queryset().exists():
            # if queryset.exists():
            leads_data = [LeadListSerializer(lead).data for lead in self.get_queryset()]
            response_data = {
                'campaign_name': self.get_queryset()[0].campaign.title,
                'leads': leads_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'success', 'message': 'No leads found'}, status=status.HTTP_200_OK)
