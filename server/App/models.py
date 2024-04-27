from django.db import models
from rest_framework import serializers

class Click(models.Model):
    is_clicked = models.BooleanField(default=False)

    def __str__(self):
        return f"Click: {self.is_clicked}"




class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        exclude = ["id"]
