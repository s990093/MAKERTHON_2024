from django.urls import path
from . import views

app_name = "Web"

from django.urls import path
from . import views

urlpatterns = [
    path('publish', views.publish_message, name='publish'),
]
