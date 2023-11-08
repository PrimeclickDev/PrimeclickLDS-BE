from django.urls import path
from .views import CampaignUploadView, LeadFormAPIView, LeadListAPIView
urlpatterns = [
    path('business/<uuid:business_id>/campaign-upload/',
         CampaignUploadView.as_view(), name='campaign-upload'),
    path('campaign/<str:campaign_id>/lead-create/',
         LeadFormAPIView.as_view(), name='lead-create'),
    path('campaign/<str:campaign_id>/leads/',
         LeadListAPIView.as_view(), name='lead-list'),

]
