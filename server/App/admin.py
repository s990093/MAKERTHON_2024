from django.contrib import admin

from App.models import *

# Register your models here.

@admin.register(PostPhoto)
class App(admin.ModelAdmin):
    pass


@admin.register(SolarDeviceData)
class SolarDeviceDataApp(admin.ModelAdmin):
    pass
