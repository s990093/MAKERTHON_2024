from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *

class AppAPIView(APIView):
    def get(self, request):
        click_instance = Click.objects.first()  # 獲取第一個 Click 實例
        serializer = ClickSerializer(click_instance)
        return Response(serializer.data)
    
    def post(self, request):
        is_click = request.data.get('isclick')  # 從 POST 請求中獲取 isclick 數據
        
        if is_click is not None:  # 確保收到了 isclick 數據
            click_instance = Click.objects.first()  # 獲取第一個 Click 實例
            if click_instance is not None:
                click_instance.is_clicked = is_click  # 更新 is_clicked 屬性
                click_instance.save()  # 保存更改
                serializer = ClickSerializer(click_instance)
                return Response(serializer.data)
            else:
                return Response({'message': 'No Click instance found.'}, status=404)
        else:
            return Response({'message': 'No isclick data provided.'}, status=400)
