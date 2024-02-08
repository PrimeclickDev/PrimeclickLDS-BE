from django.urls import path
from .views import (CallCreateAPIView, CallReportAPIView, CampaignUploadView,
                    ContactOptionAPIView, FormDesignCreateAPIView, FormDesignRetrieveAPIView, FormDesignUpdateAPIView,
                    LaunchCallAPIView, LeadDetailAPIView, LeadFormAPIView,
                    LeadListAPIView, CampaignNameAPIView, CampaignListAPIView)


urlpatterns = [
    path('campaign/upload/<uuid:business_id>/',
         CampaignUploadView.as_view(), name='campaign-upload'),
    path('campaign/add/contact/<str:campaign_id>/',
         ContactOptionAPIView.as_view(), name='contact-option'),
    path('campaign/call/create/<str:campaign_id>/',
         CallCreateAPIView.as_view(), name='campaign-call-create'),
    path('campaign/call/launch/<str:campaign_id>/',
         LaunchCallAPIView.as_view(), name='campaign-call-launch'),
    path('campaign/create/<uuid:business_id>/',
         CampaignNameAPIView.as_view(), name='campaign-name'),
    path('lead/create/<str:campaign_id>/',
         LeadFormAPIView.as_view(), name='lead-create'),
    path('leads/list/<str:campaign_id>/',
         LeadListAPIView.as_view(), name='lead-list'),
    path('leads/detail/<str:lead_id>/',
         LeadDetailAPIView.as_view(), name='lead-detail'),
    path('campaigns/list/<uuid:business_id>/',
         CampaignListAPIView.as_view(), name='campaign-list'),
    path('call-report/', CallReportAPIView.as_view(), name='call-report'),
    path('campaign/<str:campaign_id>/form-design/',
         FormDesignCreateAPIView.as_view(), name='form-design-create'),
    path('campaign/<str:campaign_id>/form-design/',
         FormDesignRetrieveAPIView.as_view(), name='retrieve_form_design'),
    path('campaign/<str:campaign_id>/form-design/',
         FormDesignUpdateAPIView.as_view(), name='update_form_design'),
]
