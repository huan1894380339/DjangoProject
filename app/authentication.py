from app.models import BlackListedToken
from rest_framework.permissions import BasePermission
from django.core.exceptions import PermissionDenied


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        import ipdb
        ipdb.set_trace()
        user_id = request.user.id
        is_allowed_user = True
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            is_blackListed = BlackListedToken.objects.get(
                user=user_id, token=token,
            )
            if is_blackListed:
                is_allowed_user = False
                raise PermissionDenied(
                    'You need login again to get new access token',
                )
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
