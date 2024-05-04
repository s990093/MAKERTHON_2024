from django.contrib import admin

from App.models import PostPhoto

# Register your models here.

@admin.register(PostPhoto)
class App(admin.ModelAdmin):
    pass