import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from app.models import TrainDetails


class YourCustomConsumerName(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

    def disconnect(self, code=None):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data=None, **kwargs):
        train_id, status = text_data.split(",")
        user = self.scope.get("user")
        if user and user.is_staff:
            TrainDetails.objects.filter(pk=train_id).update(status=status)
        content = TrainDetails.objects.values("id", "name", "status")
        response_from_server = json.dumps(list(content))
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "chat.message",
                "text": response_from_server,
            },
        )

    def chat_message(self, event):
        self.send(text_data=event["text"])
