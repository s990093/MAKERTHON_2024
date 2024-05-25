import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import datetime
from rich import pretty
from rich.console import Console

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
            # message = text_data_json.get('message')
            device = text_data_json.get('device')
            
            console.print(f"device: {text_data_json}" )

            # if device == 'camera':
            #     people_count = text_data_json.get('people_count', 0)
                
            #     # criumstane
            #     if people_count > 5:
            #         async_to_sync(self.channel_layer.group_send)(
            #             self.room_group_name,
            #             {
            #                 'type': 'trigger_alert',
            #                 'message': 'Person count exceeds 5!'
            #             }
            #         )
            
                    
            if device == 'esp8266' and bool(text_data_json.get('click', False) ) == True:
                
                # console.print(text_data_json)

                # criumstane
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'trigger_alert',
                        'message': 'Person count exceeds 5!',
                        "speed": text_data_json.get('speed')
                    }
                )
        except json.JSONDecodeError:
            console.print("Received message is not in JSON format", style="bold red")

    # def chat_message(self, event):
    #     """
    #     Method called when a chat message is received from the group.
    #     Sends the message to the WebSocket.
    #     """
    #     message = event['message']
    #     self.send(text_data=json.dumps({
    #         "message": message,
    #         "click": True,
    #         "speed": message.get('speed'),
    #         "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     }))

    def trigger_alert(self, event):
        """
        Method called when an alert is triggered.
        Sends an alert message to the WebSocket.
        """
        message = event['message']

        self.send(text_data=json.dumps({
            "message":message,
            "speed": event['speed'],
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }))
