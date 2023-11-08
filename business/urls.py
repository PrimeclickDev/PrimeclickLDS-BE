from django.urls import path
from .views import CampaignUploadView
urlpatterns = [
    path('business/<uuid:business_id>/campaign-upload/',
         CampaignUploadView.as_view(), name='campaign-upload')
]
