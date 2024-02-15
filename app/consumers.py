import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('graph_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('graph_group', self.channel_name)

    async def update_graph(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))