from django.urls import path
from .views import CampaignUploadView, LeadFormAPIView, LeadListAPIView, CampaignNameAPIView, CampaignListAPIView
urlpatterns = [
    path('campaign/upload/<uuid:business_id>/',
         CampaignUploadView.as_view(), name='campaign-upload'),
    path('campaign/create/<uuid:business_id>/',
         CampaignNameAPIView.as_view(), name='campaign-name'),
    path('lead/create/<str:campaign_id>/',
         LeadFormAPIView.as_view(), name='lead-create'),
    path('leads/list/<str:campaign_id>/',
         LeadListAPIView.as_view(), name='lead-list'),
    path('campaigns/list/<uuid:business_id>/',
         CampaignListAPIView.as_view(), name='campaign-list')

]
