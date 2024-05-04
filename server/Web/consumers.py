# myapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse

from server.App.models import PostPhotoSerializer

class FileUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # 接受连接
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # 检查是否接收了文件数据
        if bytes_data:  # 如果接收到字节数据
            filename = "uploaded_file.jpg"  # 可以动态设置
            in_memory_file = InMemoryUploadedFile(
                file=ContentFile(bytes_data),
                field_name=None,
                name=filename,
                content_type='image/jpeg',
                size=len(bytes_data),
                charset=None
            )

            data = {'photo': in_memory_file}
            serializer = PostPhotoSerializer(data=data)  # 使用适当的序列化器

            if serializer.is_valid():
                serializer.save()  # 保存序列化的数据
                response = {'status': 'success', 'message': 'File uploaded'}
            else:
                response = {'status': 'error', 'message': 'Invalid data'}

            # 发送响应
            await self.send(text_data=json.dumps(response))
        else:
            # 没有文件数据
            await self.send(text_data=json.dumps({'status': 'error', 'message': 'No file uploaded'}))
