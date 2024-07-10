from rest_framework.permissions import BasePermission
from django.utils import timezone
from .models import ViewTimeHistory


class IsLinkValid(BasePermission):
    def has_permission(self, request, view):
        # Extract email and campaign_id from URL parameters
        email = view.kwargs.get('email')
        campaign_id = view.kwargs.get('campaign_id')

        if not email or not campaign_id:
            return False

        try:
            view_link_time = ViewTimeHistory.objects.get(email=email, campaign_id=campaign_id)
        except ViewTimeHistory.DoesNotExist:
            return False

        # Check if the link is within the 12-hour window
        if timezone.now() > view_link_time.sent_time + timezone.timedelta(hours=12):
            return False

        return True
