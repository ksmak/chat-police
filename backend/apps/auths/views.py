from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from rest_framework.response import Response

from .serializers import CustomUserSerializer

User = get_user_model()


def get_user_ip(request):
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR")

    if ip_address:
        ip_address = ip_address.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR")

    return ip_address


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        ip = get_user_ip(request)
        try:
            user = User.objects.get(ip=ip)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found.")

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_name": user.name,
            }
        )


class UsersViewSet(ReadOnlyModelViewSet):
    """Users viewset."""

    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return User.objects.exclude(
            Q(username=self.request.user.username) | Q(is_superuser=True)
        )
