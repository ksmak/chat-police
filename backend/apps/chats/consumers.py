from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .tasks import (
    update_chat,
    create_message,
    read_message,
    edit_message,
    delete_message,
)


User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """Consumer for chat."""

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.user = None
        self.group_name = "chat"

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.id:
            raise ValidationError("User not found.")

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        update_chat.delay(
            group_name=self.group_name, from_id=self.user.id, is_active=True
        )

        await self.accept()

    async def disconnect(self, exit_code):
        update_chat.delay(
            group_name=self.group_name, from_id=self.user.id, is_active=False
        )

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content["message"] == "send_new":
            create_message.delay(
                group_name=self.group_name,
                message_type=content["message_type"],
                from_id=self.user.id,
                to_id=content["to_id"],
                text=content["text"],
                file=content["file"],
            )
        elif content["message"] == "send_read":
            read_message.delay(
                group_name=self.group_name,
                message_type=content["message_type"],
                from_id=self.user.id,
                message_id=content["message_id"],
            )
        elif content["message"] == "send_edit":
            edit_message.delay(
                group_name=self.group_name,
                message_type=content["message_type"],
                text=content["text"],
                message_id=content["message_id"],
            )
        elif content["message"] == "send_delete":
            delete_message.delay(
                group_name=self.group_name,
                message_type=content["message_type"],
                message_id=content["message_id"],
            )

    async def chat_message(self, event):
        await self.send_json(event)
