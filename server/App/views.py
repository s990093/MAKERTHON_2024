import json
import os
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import sys
import torch
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将 yolov5 目录添加到 Python 模块路径
yolov5_path = os.path.join(base_dir, './../yolov5')  # 相对路径至 yolov5

# # 加載 YOLO 模型
path_weightfile = f"{yolov5_path}/yolov5s.pt"
model = torch.hub.load(yolov5_path, 'custom',
                               path=path_weightfile, source='local', device='mps')
class AppAPIView(APIView):
    def get(self, request):
        click_instance = Click.objects.first() 
        serializer = ClickSerializer(click_instance)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        
        
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        uploaded_file = request.FILES['file']
        
          # 获取上传的文件
        uploaded_file = request.FILES['file']

        # 保存到临时文件夹
        file_path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))

        # 使用 YOLO 模型进行检测
        results = model(file_path)  # 使用文件路径作为输入

        json_str = results.pandas().xyxy[0].to_json(orient='records')
        
        
        detections = json.loads(json_str)
        
        
        
        
        # high_confidence_results = [r for r in detections if r['confidence'] > 0.5]
        
        # print(high_confidence_results)

      

        # 删除临时文件
        os.remove(file_path)
        
        # print(results)

        file_name = uploaded_file.name
        file_size = uploaded_file.size

        # 返回 JSON 响应
        return JsonResponse({
            'file_name': file_name,
            'file_size': file_size,
            'detections':detections[0].get("name"),
        })