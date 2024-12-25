from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from chats.models import Message
from chats.serializers import MessageSerializer, OnlineUserSerializer


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """Custom user serializer."""

    messages = serializers.SerializerMethodField()

    online = OnlineUserSerializer(source="onlineuser")

    class Meta:
        model = User
        fields = ("id", "name", "is_active", "messages", "online")

    def get_messages(self, obj):
        result = Message.objects.filter(state=Message.STATE_ACTIVE).filter(
            Q(to_chat=None) & (Q(from_user=obj.id) | Q(to_user=obj.id))
        )

        serializer = MessageSerializer(result, many=True)

        return serializer.data
