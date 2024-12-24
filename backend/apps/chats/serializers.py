from rest_framework import serializers
from .models import Message, Chat, Reader, OnlineUser
from auths.models import CustomUser


class ReaderSerializer(serializers.ModelSerializer):
    """Reader serializer model."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Reader
        fields = ("id", "message", "user", "fullname", "read_date")

    def get_fullname(self, obj):
        result = CustomUser.objects.get(id=obj.user.id)
        return result.full_name


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer model."""

    readers = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()

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
            "fullname",
        )

    def get_readers(self, obj):
        result = Reader.objects.filter(message=obj.id)
        return ReaderSerializer(result, many=True).data

    def get_fullname(self, obj):
        result = CustomUser.objects.get(id=obj.from_user.id)
        return result.full_name


class ChatSerializer(serializers.ModelSerializer):
    """Chat serializer model."""

    # messages = MessageSerializer(source='chat_messages', many=True)
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
