from django.db import models
from rest_framework import serializers

# 存储照片的模型
class PostPhoto(models.Model):
    photo = models.ImageField(upload_to='post_photos/')  # 指定照片上传目录

    def __str__(self):
        return f"Photo: {self.photo.name}"


# 序列化类
class PostPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPhoto
        fields = ['photo'] 
