import asyncio
import websockets
import json
from rich import pretty, print, print_json
from rich.console import Console

pretty.install()
console = Console()

async def client():
    uri = 'ws://127.0.0.1:8000/ws/chat/test/'
    # uri = 'ws://49.213.238.75:5000/ws/chat/test/'
    async with websockets.connect(uri) as websocket:
        # 要发送的字典
        data_to_send = {
            "device": "camera",
            "people_count": "10",
            'message': 'Hello, Server!',
        }

        # 将字典编码为JSON
        json_data = json.dumps(data_to_send)

        # 通过WebSocket发送JSON消息
        await websocket.send(json_data)
        print(f'Sent message: {json_data}')

        # 等待回应
        response = await websocket.recv()
        print(f'Received response: {response}')
        return response
