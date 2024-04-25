from django.urls import path
from .views import (AITAPIView, AITFlowAPIView, AITRecordAPIView, CallCreateAPIView, CallReportAPIView, CampaignUploadView,
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
    path('campaign/form-design/<str:campaign_id>/',
         FormDesignRetrieveAPIView.as_view(), name='retrieve-form-design'),
    path('campaign/form-design/<str:campaign_id>/update/',
         FormDesignUpdateAPIView.as_view(), name='update-form-design'),         
    path('intro/', AITAPIView.as_view(), name='ait-call-trigger'),
    path('call/user/input/', AITFlowAPIView.as_view(), name='call-user-input'),
    path('record/call/', AITRecordAPIView.as_view(), name='record-call')
]
