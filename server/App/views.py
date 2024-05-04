import json
import os
from django.shortcuts import get_object_or_404
import torch
import io
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from ultralytics import YOLO
from .models import *

# rich
from rich import pretty
from rich import print,print_json
from rich.console import Console

pretty.install()
console = Console()

# # 加载 YOLOv8 模型
# try:
#     model = YOLO('yolov8s.pt')  # 确保路径正确
#     console.log("yolov8s.pt ok")
# except Exception as e:
#     raise Exception(f"Error loading YOLO model: {str(e)}")


class AppAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        # 获取最新的 PostPhoto 对象
        latest_photo = PostPhoto.objects.order_by('-id').first() 

        if not latest_photo:
            return JsonResponse({'error': 'No photos found'}, status=404)

        # 返回 JSON 响应，包含照片的 URL
        return JsonResponse({
            'message': 'Latest photo retrieved successfully',
            'photo_url': latest_photo.photo.url 
        })
    
    def post(self, request, *args, **kwargs):
        people_count = int(request.POST.get('people_count'))
       
        console.log(f"people_count -> {people_count}")
       
            # rules
        if people_count > 0:
            id = 1
            obj = SolarDeviceData.objects.get(id=id)
            obj.people_count =people_count
            
            if people_count > 2:
                obj.is_sprinkling = True
                
            if obj.is_sprinkling == True:
                obj.is_sprinkling = False
                
            obj.save()
            
        return JsonResponse({
            'message': 'Latest photo retrieved successfully',
        })
        
         
        
        
        
        
class SolarDeviceAPIView(APIView):
        def get(self, request, id: int, *args, **kwargs):
            # 获取与特定设备 ID 相关的数据
            try:
                # 获取最新的设备数据
                device_data = SolarDeviceData.objects.filter(device_id=id).order_by('-timestamp').first()

                if not device_data:
                    # 如果找不到数据，返回 404 错误
                    return Response({"error": "No data found for this device"}, status=status.HTTP_404_NOT_FOUND)

                # 使用序列化器将数据转换为 JSON
                serializer = SolarDeviceDataSerializer(device_data)
                
                # 返回 JSON 响应
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                console.log(str(e))
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
class IpadAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            device_data = SolarDeviceData.objects.all().order_by("timestamp").values()

            if not device_data.exists():
                return Response({"error": "No data found for this device"}, status=status.HTTP_404_NOT_FOUND)

            serializer = IpadSerializer(device_data, many=True)
            return Response(data=serializer.data)

        except Exception as e:
            console.log(f"An error occurred: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            