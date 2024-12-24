from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CustomUserSerializer,
    MyTokenObtainPairSerializer,
)


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(ReadOnlyModelViewSet):
    """Users viewset."""

    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return User.objects.exclude(
            Q(username=self.request.user.username) | Q(is_superuser=True)
        )
