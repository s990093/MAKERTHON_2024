import json
import os
import torch
import io
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser

from ultralytics import YOLO
from .models import *

# rich
from rich import pretty
from rich import print,print_json
from rich.console import Console

pretty.install()
console = Console()

# 加载 YOLOv8 模型
try:
    model = YOLO('yolov8s.pt')  # 确保路径正确
    console.log("yolov8s.pt ok")
except Exception as e:
    raise Exception(f"Error loading YOLO model: {str(e)}")


class AppAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        # 获取最新的 PostPhoto 对象
        latest_photo = PostPhoto.objects.order_by('-id').first()  # 按照 ID 逆序排列，取第一个

        if not latest_photo:
            return JsonResponse({'error': 'No photos found'}, status=404)

        # 返回 JSON 响应，包含照片的 URL
        return JsonResponse({
            'message': 'Latest photo retrieved successfully',
            'photo_url': latest_photo.photo.url  # 访问照片的 URL
        })
    
    def post(self, request, *args, **kwargs):
        # 检查请求中是否有文件

        
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        # 获取上传的文件
        uploaded_file = request.FILES['file']

        # 使用序列化器，包含文件数据
        data = {
            'photo': uploaded_file,
            # 如果有其他字段需要添加，可以在这里进行
        }

        serializer = PostPhotoSerializer(data=data)
        
        # 验证和保存
        if serializer.is_valid():
            # 保存到模型
            photo_instance = serializer.save()
            
            # 使用 YOLO 进行检测
            results = model(photo_instance.photo.path, device="mps")  # 使用模型路径
            
            # 处理结果，获取所需信息
            class_names = []
            for result in results:
                class_ids = result.boxes.cls
                class_names.extend([model.names[int(cls_id)] for cls_id in class_ids])
                
            data = {
                'file_name': uploaded_file.name,
                'file_size': uploaded_file.size,
                'file_url': photo_instance.photo.url,  
                'class_names': class_names,
            }
            console.log(data)
            return JsonResponse(data, status=201)
        
        # 如果数据无效，返回错误信息
        return JsonResponse({
            'error': serializer.errors,
        }, status=400)