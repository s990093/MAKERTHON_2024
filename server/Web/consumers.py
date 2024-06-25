import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import datetime
from rich import pretty
from rich.console import Console

from App.models import *

pretty.install()
console = Console()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """
        Method called when a WebSocket connection is established.
        Initializes the chat room and adds the current channel to the group.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        Method called when the WebSocket connection is closed.
        Removes the current channel from the group.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """
        Method called when a message is received from the WebSocket.
        Processes the message and sends it to the group if it is valid.
        """
        try:
            text_data_json = json.loads(text_data)
            device = text_data_json.get('device', "none")
            
            if device == 'ESP32':
                brightness = text_data_json.get('brightness')
                
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_brightness',
                        'brightness': brightness
                    }
                )
            
            elif device == 'ipad':
                # 根据 iPad 的逻辑进行处理，这里假设要发送特定的数据
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'send_ipad_data',
                        'message': 'Data for iPad'
                    }
                )
                
        except json.JSONDecodeError:
            console.print("Received message is not in JSON format", style="bold red")

    def send_brightness(self, event):
        """
        Method called to send Arduino brightness data to the WebSocket.
        """
        brightness = event['brightness']
        
        self.send(text_data=json.dumps({
            'device': 'arduino',
            'brightness': brightness,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }))
    
    def send_ipad_data(self, event):
        """
        Method called to send iPad data to the WebSocket.
        """
        message = event['message']
        
        self.send(text_data=json.dumps({
            'device': 'ipad',
            'message': message,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }))
