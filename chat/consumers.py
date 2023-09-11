import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer, AcceptConnection, DenyConnection, \
    InvalidChannelLayerError
from django.db.models import Q

from chat import models


class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, message):
        try:
            self.chat_room = str(self.scope["user"].pk)
            await self.channel_layer.group_add(self.chat_room, self.channel_name)
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        try:
            await self.connect()
        except AcceptConnection:
            await self.accept()
        except DenyConnection:
            await self.close()

    async def websocket_receive(self, message):
        data = json.loads(message["text"])
        sender = self.scope["user"]
        uuid = self.scope["path"].split("/")[2]
        try:
            thread = await models.Thread.objects.select_related("owner", "candidate").aget(
                Q(owner=sender) | Q(candidate=sender), uuid=uuid, is_active=True
            )
            if thread.owner == sender:
                receiver = thread.candidate
            else:
                receiver = thread.owner
            new_message = await models.Message.objects.acreate(
                thread=thread, owner=sender, message=data.get("message")
            )
            thread.updated_at = new_message.created_at
            await thread.asave()
        except Exception as e:
            return await self.send({"type": "websocket.close"})
        created_at = new_message.created_at
        sender_response = {
            "message_pk": new_message.pk,
            "message": data.get("message"),
            "sender_pk": sender.pk,
            "created_at":  created_at.astimezone(sender.timezone).strftime("%m/%d/%y %H:%M")
        }
        receiver_response = {
            "message_pk": new_message.pk,
            "message": data.get("message"),
            "sender_pk": sender.pk,
            "created_at":  created_at.astimezone(receiver.timezone).strftime("%m/%d/%y %H:%M")
        }
        await self.channel_layer.group_send(
            self.chat_room,
            {"type": "chat_message", "text": json.dumps(sender_response)},
        )
        await self.channel_layer.group_send(
            str(receiver.pk),
            {"type": "chat_message", "text": json.dumps(receiver_response)},
        )

    async def chat_message(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})

    async def send(self, text_data=None, bytes_data=None, close=False):
        await self.base_send(text_data)

    async def websocket_disconnect(self, message):
        try:
            await self.channel_layer.group_discard(self.chat_room, self.channel_name)
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        await self.disconnect(message["code"])
        raise StopConsumer()
