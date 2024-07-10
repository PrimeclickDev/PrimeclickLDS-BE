from rest_framework.permissions import BasePermission
from django.utils import timezone
from .models import ViewTimeHistory


class IsLinkValid(BasePermission):
    def has_permission(self, request, view):
        # Extract email and campaign_id from URL parameters
        path = view.kwargs.get('path')
        campaign_id = view.kwargs.get('campaign_id')

        if not path or not campaign_id:
            return False

        try:
            view_link_time = ViewTimeHistory.objects.get(path=path, campaign_id=campaign_id)
        except ViewTimeHistory.DoesNotExist:
            return False

        # # Check if the link is within the 12-hour window
        # if timezone.now() > view_link_time.sent_time + timezone.timedelta(hours=12):
        #     return False

        return True
