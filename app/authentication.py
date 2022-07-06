from app.models import BlackListedToken
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied


class IsTokenValid(IsAuthenticated):
    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True
        if request.headers.get('Authorization') is None:
            raise PermissionDenied(
                'Authentication credentials were not provided',
            )
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            is_blackListed = BlackListedToken.objects.select_related('user').get(
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
