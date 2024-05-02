import json
import os
import torch
import io
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ultralytics import YOLO
from .models import Click
from .models import ClickSerializer


# 加载 YOLOv8 模型
try:
    model = YOLO('yolov8s.pt')  # 确保路径正确
except Exception as e:
    raise Exception(f"Error loading YOLO model: {str(e)}")


class AppAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file_path = None  # 初始化变量以便在 finally 中访问
        
        try:
            if 'file' not in request.FILES:
                return JsonResponse({'error': 'No file uploaded'}, status=400)

            uploaded_file = request.FILES['file']

            # 保存到临时文件夹
            file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))

            # 使用 YOLO 进行检测
            results = model(file_path, device="mps")  # 假设模型需要文件路径

            # 处理结果，获取所需信息
            class_names = []
            for result in results:
                class_ids = result.boxes.cls
                class_names.extend([model.names[int(cls_id)] for cls_id in class_ids])

            # 返回 JSON 响应
            return JsonResponse({
                'file_name': uploaded_file.name,
                'file_size': uploaded_file.size,
                'class_names': class_names,
            })

        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)

        finally:
            if file_path and os.path.exists(file_path):  # 确保文件存在
                os.remove(file_path)