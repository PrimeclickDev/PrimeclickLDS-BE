from rest_framework.permissions import BasePermission
from django.utils import timezone
from .models import ViewTimeHistory


class IsLinkValid(BasePermission):
    def has_permission(self, request, view):
        # Extract access_code and campaign_id from URL parameters
        access_code = view.kwargs.get('access_code')
        campaign_id = view.kwargs.get('campaign_id')

        # Ensure both access_code and campaign_id are present
        if not access_code or not campaign_id:
            return False

        # Check if access is valid for the given access_code and campaign_id
        try:
            access_record = ViewTimeHistory.objects.get(
                access_code=access_code,
                campaign_id=campaign_id,
                has_access=True
            )
            return True
        except ViewTimeHistory.DoesNotExist:
            return False
        except Exception as e:
            # Optionally log the unexpected error for debugging
            return False


class IsAdminOrSuperadmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser