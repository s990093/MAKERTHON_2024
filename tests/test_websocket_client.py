import unittest
import asyncio

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
            "device": "esp32",
            "click": True,
            'message': '', 
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

# class TestWebSocketClient(unittest.TestCase):

#     def test_client_response(self):
#         loop = asyncio.get_event_loop()
#         response = loop.run_until_complete(client())
        
#         # 在这里，你可以根据你的需求对response进行断言
#         self.assertIn('Hello, Client!', response)

# if __name__ == '__main__':
#     unittest.main()

asyncio.run(client())