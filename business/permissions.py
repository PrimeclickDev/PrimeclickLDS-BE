from rest_framework.permissions import BasePermission
from django.utils import timezone
from .models import ViewTimeHistory


class IsLinkValid(BasePermission):
    def has_permission(self, request, view):
        # Extract email and campaign_id from URL parameters
        access_code = view.kwargs.get('access_code')
        campaign_id = view.kwargs.get('campaign_id')

        if not access_code or not campaign_id:
            return False

        try:
            ViewTimeHistory.objects.get(access_code=access_code, campaign_id=campaign_id)
        except ViewTimeHistory.DoesNotExist:
            return False

        return True
