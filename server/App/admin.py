from django.contrib import admin

from App.models import Click

# Register your models here.

@admin.register(Click)
class App(admin.ModelAdmin):
    pass