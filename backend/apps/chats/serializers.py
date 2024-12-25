from rest_framework import serializers
from .models import Message, Chat, Reader, OnlineUser
from auths.models import CustomUser


class ReaderSerializer(serializers.ModelSerializer):
    """Reader serializer model."""

    name = serializers.SerializerMethodField()

    class Meta:
        model = Reader
        fields = ("id", "message", "user", "name", "read_date")

    def get_name(self, obj):
        return obj.user.name


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer model."""

    readers = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "state",
            "from_user",
            "to_user",
            "to_chat",
            "text",
            "file",
            "created_at",
            "changed_at",
            "deleted_at",
            "readers",
            "name",
        )

    def get_readers(self, obj):
        result = Reader.objects.filter(message=obj.id)
        return ReaderSerializer(result, many=True).data

    def get_name(self, obj):
        return obj.from_user.name


class ChatSerializer(serializers.ModelSerializer):
    """Chat serializer model."""

    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat

        fields = ("id", "title", "users", "actives", "created_at", "messages")

    def get_messages(self, obj):
        result = Message.objects.filter(state=Message.STATE_ACTIVE, to_chat=obj.id)
        serializer = MessageSerializer(result, many=True)
        return serializer.data


class OnlineUserSerializer(serializers.ModelSerializer):
    """Serializer for online users."""

    class Meta:
        model = OnlineUser
        fields = ("user", "is_active", "last_date")
