from django.urls import path
from . import views

app_name = "App"


urlpatterns = [
    path("", views.AppAPIView.as_view(), name="AppAPIView")
    ]
