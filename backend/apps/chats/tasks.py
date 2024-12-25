from django.contrib.auth import get_user_model
from django.utils import timezone
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Chat, Message, OnlineUser
from .serializers import MessageSerializer, OnlineUserSerializer


@shared_task
def update_chat(
    group_name: str,
    from_id: int,
    is_active: bool,
):
    online_user = OnlineUser.objects.get_or_create(user=from_id)[0]
    online_user.is_active = is_active
    online_user.save()

    serializer = OnlineUserSerializer(online_user)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "category": "change_chat",
            "online_user": serializer.data,
        },
    )


@shared_task
def create_message(
    group_name: str,
    message_type: str,
    from_id: int,
    to_id: int,
    text: str,
    file: str,
) -> None:

    to_user = None
    to_chat = None

    if message_type == "user":
        to_user = get_user_model().objects.get(id=to_id)
    else:
        to_chat = Chat.objects.get(id=to_id)

    from_user = get_user_model().objects.get(id=from_id)

    message = Message.objects.create(
        from_user=from_user,
        to_user=to_user,
        to_chat=to_chat,
        text=text,
    )

    if file:
        message.file.name = file
        message.save()

    serializer = MessageSerializer(message)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "category": "new_message",
            "message_type": message_type,
            "message": serializer.data,
        },
    )


@shared_task
def read_message(
    group_name: str,
    message_type: str,
    from_id: int,
    message_id: str,
) -> None:

    from_user = get_user_model().objects.get(id=from_id)

    message = Message.objects.get(id=message_id)
    message.readers.add(from_user)
    message.save()

    serializer = MessageSerializer(message)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "category": "change_message",
            "message_type": message_type,
            "message": serializer.data,
        },
    )


@shared_task
def edit_message(
    group_name: str,
    message_type: str,
    text: str,
    message_id: str,
) -> None:

    message = Message.objects.get(id=message_id)
    message.text = text
    message.save()

    serializer = MessageSerializer(message)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "category": "change_message",
            "message_type": message_type,
            "message": serializer.data,
        },
    )


@shared_task
def delete_message(
    group_name: str,
    message_type: str,
    message_id: str,
) -> None:

    message = Message.objects.get(id=message_id)
    message.state = Message.STATE_DELETE
    message.save()

    serializer = MessageSerializer(message)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "category": "change_message",
            "message_type": message_type,
            "message": serializer.data,
        },
    )


@shared_task
def clean_chat():
    Message.objects.filter(
        modified_date__lt=timezone.now() - timezone.timedelta(days=1)
    ).delete()
